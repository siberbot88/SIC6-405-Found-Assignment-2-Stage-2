import network
import urequests
import utime
from machine import Pin, ADC, Timer
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

# Inisialisasi Sensor dan Aktuator
sensor_dht = dht.DHT11(Pin(5))
sensor_pir = Pin(19, Pin.IN)
sensor_ldr = ADC(Pin(34))
sensor_ldr.atten(ADC.ATTN_11DB)
buzzer = Pin(21, Pin.OUT)

# Inisialisasi LED
led_yellow = Pin(2, Pin.OUT)
led_red = Pin(12, Pin.OUT)

# Inisialisasi Tombol dan LED Sistem
button = Pin(18, Pin.IN, Pin.PULL_DOWN)
led_system = Pin(4, Pin.OUT)
system_active = False
led_system.value(system_active)

# Variabel debouncing
last_press_time = 0
debounce_time = 200

# Variabel timing
last_ldr_time = 0
last_dht_time = 0
ldr_interval = 500
dht_interval = 5000

# Variabel penyimpanan data
current_temp = 0
current_hum = 0
current_motion = 0
current_status = "suhu aman"

def button_pressed(pin):
    global system_active, last_press_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_press_time) >= debounce_time:
        system_active = not system_active
        led_system.value(system_active)
        last_press_time = current_time

button.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)

url = "http://192.168.43.89:5000/sensor1"

def control_leds(ldr_value):
    if ldr_value > 4000:
        led_yellow.off()
        led_red.off()
    else:
        led_yellow.on()
        led_red.value(not led_red.value())

while True:
    if system_active:
        try:
            now = utime.ticks_ms()
            
            # Update sensor DHT dan kontrol buzzer
            if utime.ticks_diff(now, last_dht_time) >= dht_interval:
                sensor_dht.measure()
                current_temp = sensor_dht.temperature()
                current_hum = sensor_dht.humidity()
                current_motion = sensor_pir.value()
                
                # Kontrol buzzer dan status
                if current_temp > 32:
                    buzzer.on()
                    current_status = "suhu tinggi"
                else:
                    buzzer.off()
                    current_status = "suhu aman"
                
                last_dht_time = now
                print("Memperbarui data DHT/PIR")
            
            # Pembacaan dan pengiriman data LDR
            if utime.ticks_diff(now, last_ldr_time) >= ldr_interval:
                ldr_value = sensor_ldr.read()
                control_leds(ldr_value)
                
                data = {
                    "temperature": current_temp,
                    "humidity": current_hum,
                    "motion": current_motion,
                    "ldr": ldr_value,
                    "status": current_status
                }
                
                print("Mengirim data:", data)
                response = urequests.post(url, json=data)
                response.close()
                last_ldr_time = now
                
            utime.sleep_ms(50)
            
        except Exception as e:
            print("Error:", e)
            utime.sleep(1)
    else:
        buzzer.off()
        led_yellow.off()
        led_red.off()
        utime.sleep(0.1)