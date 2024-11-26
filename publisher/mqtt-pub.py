import paho.mqtt.client as mqtt
import random
import time
import json
from datetime import datetime

# Konfigurasi MQTT
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPICS = ["v2.0/subs/APP64f7e28a5964d54552/DEV650bfd4fb68de46441", "v2.0/subs/APP64f7e28a5964d54552/DEV650c04ed6097879912", "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd518fdbd25357", "v2.0/subs/APP64f7e28a5964d54552/DEV650bfd505a3a394189"]

# Callback ketika berhasil terkoneksi
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Berhasil terkoneksi ke broker MQTT")
    else:
        print(f"Gagal terkoneksi, return code: {rc}")

# Callback ketika berhasil publish
def on_publish(client, userdata, mid):
    print(f"Pesan berhasil dipublish")

# Inisialisasi client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Koneksi ke broker
print("Menghubungkan ke broker MQTT...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Mulai loop client di background
client.loop_start()

# Inisialisasi counter
counter = 1

try:
    while True:
        for topic in MQTT_TOPICS:
            # Membuat payload dalam format yang diminta
            payload = {
                "counter": counter,
                "data": json.dumps({
                    "meter_type": "mk10m",
                    "data_type": "instant data",
                    "reading_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "meter_serial_number": round(random.randint(10000, 100000)),
                    "active_energy_import": round(random.randint(0, 100000)),
                    "active_energy_export": 0,
                    "reactive_energy_import": round(random.randint(80000, 100000)),
                    "reactive_energy_export": 0,
                    "apparent_energy_import": round(random.randint(100000000, 110000000)),
                    "apparent_energy_export": 0,
                    "instantaneous_voltage_L1": round(random.uniform(220.0, 230.0), 3),
                    "instantaneous_voltage_L2": round(random.uniform(220.0, 230.0), 3),
                    "instantaneous_voltage_L3": round(random.uniform(220.0, 230.0), 3),
                    "instantaneous_current_L1": round(random.uniform(0.3, 0.5), 3),
                    "instantaneous_current_L2": round(random.uniform(0.3, 0.5), 3),
                    "instantaneous_current_L3": round(random.uniform(0.3, 0.5), 3),
                    "instantaneous_net_frequency": round(random.uniform(49.9, 50.1), 2),
                    "instantaneous_power_factor": round(random.uniform(0.08, 1.0), 4),
                    "create_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "raw": "0f80000000000212167016c806671c254b0a09323531343030333231150000000002f9d3a015000000000000000015000000000001421d150000000001a95f9a1500000000064a2b531500000000000000000600037b790600037bba06000382ee06000001830600000193060000019e1213850500000382"
                }),
                "devEui": "123494e68681e40c",
                "port": 11,
                "radio": {
                    "modulation": {
                        "bandwidth": 125000,
                        "type": "LORA",
                        "spreading": 8,
                        "coderate": "4/5"
                    },
                    "hardware": {
                        "status": 1,
                        "chain": 0,
                        "tmst": 0,
                        "snr": 1,
                        "rssi": -114,
                        "channel": 0,
                        "gps": {
                            "lat": -6.237232685089111,
                            "lng": 106.79916381835938,
                            "alt": 12
                        }
                    },
                    "freq": 921.8,
                    "datarate": 4,
                    "time": time.time()
                },
                "type": "uplink"
            }
            
            # Convert payload ke JSON string untuk publikasi dan log
            payload_json = json.dumps(payload)
            
            # Publish pesan
            result = client.publish(topic, payload_json)
            
            # Cek status publish
            if result[0] == 0:
                print(f"Data terkirim ke {topic}: {payload_json}")
            else:
                print("Gagal mengirim data")
            
            # Tunggu 1 detik sebelum ke topik berikutnya
            time.sleep(1)
        
        # Increment counter
        counter += 1
        time.sleep(600) 

except KeyboardInterrupt:
    print("\nMenghentikan program...")
    client.loop_stop()
    client.disconnect()
    print("Program berhenti")
