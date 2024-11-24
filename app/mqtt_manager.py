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
        self.mqtt_client.username_pw_set("193006f7395541fc", "193006f7396ceeea")
        self.mqtt_client.connect("mqtt.telkomiot.id", 1883, 18000)

        self.topics = {
            "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd4fb68de46441": "Chiller_Witel_Jaksel",
            "v2.0/subs/APP64f7e28a5964d54552/DEV650c04ed6097879912": "Lift_Witel_Jaksel",
            "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd518fdbd25357": "Lift_OPMC",
            "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd505a3a394189": "AHU_Lantai_2"
        }

        # Store last two records for each location
        self.last_two_records = {
            "Chiller_Witel_Jaksel": [None, None],
            "Lift_Witel_Jaksel": [None, None],
            "Lift_OPMC": [None, None],
            "AHU_Lantai_2": [None, None]
        }

    """
        Connect callback
    """
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in self.topics:
                self.mqtt_client.subscribe(topic, qos=2)
                print(f"Subscribed to '{topic}' topic")
        else:
            print(f"Failed to connect, return code: {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")
        if rc != 0:
            self.reconnect(client)

    def reconnect(self, client):
        while True:
            try:
                print("Attempting to reconnect...")
                for topic in self.topics:
                    self.mqtt_client.subscribe(topic, qos=2)
                    print(f"Subscribed to '{topic}' topic")
                break
            except Exception as e:
                print(f"Reconnect failed: {e}")
                time.sleep(3)

    """
        Message callback
    """
    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            raw_data = payload.get("data")
            data = json.loads(raw_data)
            position = None

            for topic, pos in self.topics.items():
                if msg.topic == topic:
                    position = pos
                    print(f"{datetime.now()} : Message from {msg.topic}")
                    break
            else:
                print(f"Unhandled topic: {msg.topic}")
                return
          
            # Update last two records
            self.last_two_records[position].append(data)
            self.last_two_records[position] = self.last_two_records[position][-2:]

            prev_data = self.last_two_records[position][0]
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

                self.db_manager.save_energy_data(diff_data)
        except json.JSONDecodeError:
            print("Error: Payload is not valid JSON")
        except KeyError as e:
            print(f"Error: Required field not found - {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    """
        MQTT loop
    """
    def start_mqtt_loop(self):
        self.mqtt_client.loop_start()
