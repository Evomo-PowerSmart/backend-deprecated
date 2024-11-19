# mqtt_service.py
from db_manager import DatabaseManager
from mqtt_manager import MQTTManager

def run_mqtt_service():
    db_manager = DatabaseManager()
    mqtt_manager = MQTTManager(db_manager)
    mqtt_manager.mqtt_client.loop_forever()

if __name__ == "__main__":
    run_mqtt_service()
