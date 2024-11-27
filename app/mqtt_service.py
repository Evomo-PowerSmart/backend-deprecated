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

def run_mqtt_service():
    """
    Initialize and run the MQTT service with proper error handling.
    """
    try:
        # Setup logging first
        setup_logging()
        logging.info("Starting MQTT Service...")

        # Initialize database manager and MQTT manager
        db_manager = DatabaseManager()
        mqtt_manager = MQTTManager(db_manager)

        # Start MQTT loop
        logging.info("Starting MQTT client loop...")
        mqtt_manager.start_mqtt_loop()

        # Keep the main thread running
        mqtt_manager.mqtt_client.loop_forever()

    except Exception as e:
        logging.error(f"Critical error in MQTT service: {e}", exc_info=True)
        sys.exit(1)

def graceful_shutdown(mqtt_manager):
    """
    Perform cleanup when the service is stopping.
    """
    logging.info("Performing graceful shutdown...")
    mqtt_manager.cleanup()

if __name__ == "__main__":
    try:
        run_mqtt_service()
    except KeyboardInterrupt:
        logging.info("MQTT Service stopped by user.")
        sys.exit(0)