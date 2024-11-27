import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime, timedelta
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import logging
from typing import Dict, List, Optional
import threading
import subprocess

class MQTTManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.username_pw_set("193006f7395541fc", "193006f7396ceeea")
        self.mqtt_client.connect("mqtt.telkomiot.id", 1883, 18000)
        
        # Initialize topics
        self.topics = {
            "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd4fb68de46441": "Chiller_Witel_Jaksel",
            "v2.0/subs/APP64f7e28a5964d54552/DEV650c04ed6097879912": "Lift_Witel_Jaksel",
            "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd518fdbd25357": "Lift_OPMC",
            "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd505a3a394189": "AHU_Lantai_2"
        }

        # Initialize message processing components
        self.message_queue = Queue(maxsize=1000)
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.processing_thread = threading.Thread(target=self._process_message_queue, daemon=True)
        

        # Use a thread-safe dictionary for last records
        self.last_two_records: Dict[str, List[Optional[dict]]] = {
            position: [None, None] for position in self.topics.values()
        }
        self.records_lock = threading.Lock()

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Start threads
        self.processing_thread.start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker")
            for topic in self.topics:
                self.mqtt_client.subscribe(topic, qos=2)
                logging.info(f"Subscribed to '{topic}' topic")
            
            # Reset last message time on successful connection
            self.last_message_time = datetime.now(timezone('Asia/Jakarta'))
        else:
            logging.error(f"Failed to connect, return code: {rc}")

    def on_disconnect(self, client, userdata, rc):
        logging.warning(f"Disconnected with result code {rc}")
        if rc != 0:
            self.reconnect(client)

    def reconnect(self, client):
        while True:
            try:
                logging.info("Attempting to reconnect...")
                client.reconnect()
                for topic in self.topics:
                    self.mqtt_client.subscribe(topic, qos=2)
                    logging.info(f"Resubscribed to '{topic}' topic")
                
                # Reset last message time on successful reconnection
                self.last_message_time = datetime.now(timezone('Asia/Jakarta'))
                break
            except Exception as e:
                logging.error(f"Reconnect failed: {e}")
                time.sleep(3)

    def on_message(self, client, userdata, msg):
        """Quick handler that just queues messages for processing"""
        try:
            current_time = datetime.now(timezone('Asia/Jakarta'))
            
            # Update last message time
            self.last_message_time = current_time
            
            logging.info(f"{current_time} : Message received from {msg.topic}")
            
            # Add to queue for processing
            self.message_queue.put_nowait((msg.topic, msg.payload.decode()))
            
        except Exception as e:
            logging.error(f"Error queueing message: {e}")

    def _process_message_queue(self):
        """Background thread to process queued messages"""
        while True:
            try:
                message_data = self.message_queue.get()
                if message_data is None:
                    break
                
                self.executor.submit(self._process_single_message, message_data)
                
            except Exception as e:
                logging.error(f"Error processing message from queue: {e}")

    def _process_single_message(self, message_data):
        """Process a single message in a separate thread"""
        try:
            topic, payload_str = message_data
            
            # Parse JSON data
            payload = json.loads(payload_str)
            raw_data = payload.get("data")
            if not raw_data:
                return
                
            data = json.loads(raw_data)
            position = self.topics.get(topic)
            
            if not position:
                logging.warning(f"Unhandled topic: {topic}")
                return

            # Update last two records with thread safety
            with self.records_lock:
                current_records = self.last_two_records[position]
                current_records.append(data)
                current_records = current_records[-2:]
                self.last_two_records[position] = current_records
                
                if current_records[0]:  # If we have a previous record
                    diff_data = self._calculate_diff(current_records[0], current_records[1], position)
                    self.db_manager.save_energy_data(diff_data)

        except json.JSONDecodeError:
            logging.error("Error: Payload is not valid JSON")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def _calculate_diff(self, prev_data, current_data, position):
        """Calculate the difference between two readings"""
        return {
            "reading_time": current_data.get("reading_time"),
            "position": position,
            "meter_type": current_data.get("meter_type"),
            "meter_serial_number": current_data.get("meter_serial_number"),
            "active_energy_import": current_data.get("active_energy_import") - prev_data.get("active_energy_import", 0),
            "active_energy_export": current_data.get("active_energy_export") - prev_data.get("active_energy_export", 0),
            "reactive_energy_import": current_data.get("reactive_energy_import") - prev_data.get("reactive_energy_import", 0),
            "reactive_energy_export": current_data.get("reactive_energy_export") - prev_data.get("reactive_energy_export", 0),
            "apparent_energy_import": current_data.get("apparent_energy_import") - prev_data.get("apparent_energy_import", 0),
            "apparent_energy_export": current_data.get("apparent_energy_export") - prev_data.get("apparent_energy_export", 0)
        }

    def cleanup(self):
        """Cleanup method to be called when shutting down"""
        self.message_queue.put(None) 
        self.processing_thread.join()
        self.executor.shutdown(wait=True)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()