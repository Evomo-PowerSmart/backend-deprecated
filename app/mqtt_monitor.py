import threading
import time
import subprocess
import logging
from datetime import datetime, timedelta

class MQTTConnectionMonitor:
    def __init__(self, mqtt_manager, check_interval=1200, restart_threshold=1200):  # 20 menit = 1200 detik
        self.mqtt_manager = mqtt_manager
        self.check_interval = check_interval
        self.restart_threshold = restart_threshold
        self.last_message_time = datetime.now()
        self.monitor_thread = None
        self._stop_event = threading.Event()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='mqtt_connection_monitor.log',
            filemode='a'
        )
        
        # Wrapper untuk on_message asli
        self._original_on_message = self.mqtt_manager.on_message
        self.mqtt_manager.on_message = self._update_last_message_time

    def _update_last_message_time(self, client, userdata, msg):
        # Update waktu terakhir menerima pesan
        self.last_message_time = datetime.now()
        # Panggil fungsi asli on_message
        return self._original_on_message(client, userdata, msg)

    def _connection_monitor_loop(self):
        while not self._stop_event.is_set():
            try:
                # Cek apakah sudah melebihi waktu threshold tanpa pesan
                time_since_last_message = datetime.now() - self.last_message_time
                
                if time_since_last_message > timedelta(seconds=self.restart_threshold):
                    logging.warning(f"No MQTT messages for {time_since_last_message}. Restarting supervisor.")
                    self._restart_supervisor()
                
                # Tunggu sebelum cek berikutnya
                self._stop_event.wait(self.check_interval)

            except Exception as e:
                logging.error(f"Error in connection monitoring loop: {e}")
                self._stop_event.wait(self.check_interval)

    def _restart_supervisor(self):
        try:
            # Perintah restart supervisor (sesuaikan dengan nama aplikasi Anda)
            subprocess.run(['sudo', 'supervisorctl', 'restart', 'flask_app'], check=True)
            logging.info("Supervisor restarted successfully")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to restart supervisor: {e}")
        except Exception as e:
            logging.error(f"Unexpected error restarting supervisor: {e}")

    def start(self):
        if not self.monitor_thread or not self.monitor_thread.is_alive():
            self._stop_event.clear()
            self.monitor_thread = threading.Thread(target=self._connection_monitor_loop, daemon=True)
            self.monitor_thread.start()
            logging.info("MQTT Connection Monitor started")

    def stop(self):
        if self.monitor_thread and self.monitor_thread.is_alive():
            self._stop_event.set()
            self.monitor_thread.join()
            logging.info("MQTT Connection Monitor stopped")

        # Kembalikan on_message ke fungsi asli
        if hasattr(self.mqtt_manager, 'on_message'):
            self.mqtt_manager.on_message = self._original_on_message