import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

"""
    MQTT handler
"""
class MQTTManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect("34.44.202.231", 1883, 65000)

        self.topics = {
            "evomo/raw_data/loc_a": "A",
            "evomo/raw_data/loc_b": "B",
            "evomo/raw_data/loc_c": "C"
        }

        self.previous_data = {
            "A": None,
            "B": None,
            "C": None
        }

    """
        Connect callback
    """
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"{datetime.now()}: Connected to MQTT broker")
            for topic in self.topics:
                self.mqtt_client.subscribe(topic, qos=2)
                print(f"{datetime.now()}: Subscribed to '{topic}' topic")
        else:
            print(f"{datetime.now()}: Failed to connect, return code: {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"{datetime.now()}: Disconnected with result code {rc}")
        if rc != 0:
            self.reconnect(client)

    def reconnect(self, client):
        while True:
            try:
                print(f"{datetime.now()}: Attempting to connect with broker...")
                client.connect("34.42.59.154", 1883, 3600)
                print(f"{datetime.now()}: Attempting to subscribe topic...")
                for topic in self.topics:
                    self.mqtt_client.subscribe(topic, qos=2)
                    print(f"{datetime.now()}: Subscribed to '{topic}' topic")
                break
            except Exception as e:
                print(f"{datetime.now()}: Reconnect failed: {e}")
                time.sleep(3)


    """
        Message callback
    """
    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            data = payload.get("data")
            position = None

            for topic, pos in self.topics.items():
                if msg.topic == topic:
                    position = pos
                    break
            else:
                print(f"{datetime.now()}: Unhandled topic: {msg.topic}")
                return
            
            prev_data = self.previous_data[position]

            if prev_data:
                diff_data = {
                    "reading_time": data.get("reading_time"),
                    "position": position,
                    "meter_type": data.get("meter_type"),
                    "meter_serial_number": data.get("meter_serial_number"),
                    "active_energy_import": data.get("active_energy_import") - prev_data.get("active_energy_import"),
                    "active_energy_export": data.get("active_energy_export") - prev_data.get("active_energy_export"),
                    "reactive_energy_import": data.get("reactive_energy_import") - prev_data.get("reactive_energy_import"),
                    "reactive_energy_export": data.get("reactive_energy_export") - prev_data.get("reactive_energy_export"),
                    "apparent_energy_import": data.get("apparent_energy_import") - prev_data.get("apparent_energy_import"),
                    "apparent_energy_export": data.get("apparent_energy_export") - prev_data.get("apparent_energy_export")
                }

                self.db_manager.save_energy_data(diff_data, position)

                result = self.mqtt_client.publish(f"evomo/final_data/loc_{position.lower()}", json.dumps(diff_data), qos=2)
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"{datetime.now()}: Data from {msg.topic} published to evomo/final_data/loc_{position.lower()}")
                else:
                    print(f"{datetime.now()}: Failed to publish data")

            self.previous_data[position] = data

        except json.JSONDecodeError:
            print(f"{datetime.now()}: Error: Payload is not valid JSON")
        except KeyError as e:
            print(f"{datetime.now()}: Error: Required field not found - {e}")
        except Exception as e:
            print(f"{datetime.now()}: Unexpected error: {e}")

    """
        MQTT loop
    """
    def start_mqtt_loop(self):
        self.mqtt_client.loop_start()
