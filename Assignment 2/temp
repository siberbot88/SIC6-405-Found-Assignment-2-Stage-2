import network
import urequests
import utime
from machine import Pin
import dht


SSID = "esp32"
PASSWORD = "none1234"

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while not station.isconnected():
    print("Menghubungkan ke WiFi...")
    utime.sleep(1)

print("Terhubung ke WiFi:", station.ifconfig())

# Inisialisasi Sensor
sensor_dht = dht.DHT11(Pin(5))
sensor_pir = Pin(19, Pin.IN) 

# Flask API URL
url = "http://192.168.43.89:5000/sensor1"  
while True:
    try:
        # Baca Sensor 
        sensor_dht.measure()
        temperature = sensor_dht.temperature()
        humidity = sensor_dht.humidity()
        motion_detected = sensor_pir.value()  # 1 jika ada gerakan, 0 jika tidak

        # Kirim Data
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "motion": motion_detected 
        }

        print("Mengirim data:", data)
        response = urequests.post(url, json=data)
        print("Response:", response.text)
        response.close()

    except Exception as e:
        print("Error:", e)

    utime.sleep(5) 


