import logging
import sys
from db_manager import DatabaseManager
from mqtt_handler import MQTTManager

def setup_logging():
    """Configure logging for the MQTT service."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('mqtt_service.log')
        ]
    )

setup_logging()
logging.info("Starting MQTT Service...")

db_manager = DatabaseManager()
mqtt_manager = MQTTManager(db_manager)

if __name__ == "__main__":
    try:
        logging.info("Starting MQTT client loop...")
        mqtt_manager.mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logging.info("MQTT Service stopped by user.")
        mqtt_manager.cleanup()
        sys.exit(0)