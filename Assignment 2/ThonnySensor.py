import network
import urequests
import utime
from machine import Pin
import dht
import machine

SSID = "esp32"
PASSWORD = "none1234"
MAX_WIFI_RETRIES = 10  # Batasi retry WiFi

# Inisialisasi Sensor
sensor_dht = dht.DHT11(Pin(5))
sensor_pir = Pin(19, Pin.IN)
url = "http://192.168.43.89:5050/sensor1"  # Pastikan IP benar

def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    
    if not station.isconnected():
        print(f"Menghubungkan ke WiFi {SSID}...")
        station.connect(SSID, PASSWORD)
        
        retries = 0
        while not station.isconnected() and retries < MAX_WIFI_RETRIES:
            print(".")
            utime.sleep(2)
            retries += 1
        
        if not station.isconnected():
            print("Gagal konek WiFi, reboot...")
            machine.reset()  # Reboot jika gagal
    
    print("Terhubung ke WiFi:", station.ifconfig())

# Main Program
try:
    connect_wifi()
    
    # Test koneksi ke server
    try:
        print("Testing server...")
        response = urequests.get(url.replace('/sensor1', '/test'), timeout=5)
        print("Server OK:", response.text)
        response.close()
    except Exception as e:
        print("Server test error:", e)
        machine.reset()

    while True:
        try:
            sensor_dht.measure()
            data = {
                "temperature": sensor_dht.temperature(),
                "humidity": sensor_dht.humidity(),
                "motion": sensor_pir.value()
            }
            
            print("Mengirim data:", data)
            response = urequests.post(url, json=data, timeout=10)  # Tambah timeout
            print("Response:", response.text)
            response.close()
            
        except OSError as e:
            print("Error koneksi:", e)
            # Coba reconnect WiFi
            connect_wifi()
        except Exception as e:
            print("Error lain:", e)
        
        utime.sleep(5)

except Exception as e:
    print("Fatal error:", e)
    machine.reset()