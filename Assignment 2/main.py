from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import threading

app = Flask(__name__)

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-MClajoBNluAp2Bkkpj1eVLYzrX8LAU"
UBIDOTS_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/sic6-esp32ee"

# Fungsi background untuk Ubidots
def send_to_ubidots_async(payload):
    try:
        headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
        response = requests.post(UBIDOTS_URL, json=payload, headers=headers, timeout=10)
        print(f"Ubidots Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print("Error Ubidots:", e)

@app.route('/sensor1', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if not data or 'temperature' not in data or 'humidity' not in data or 'motion' not in data:
        return jsonify({"error": "Data tidak lengkap"}), 400
    
    # Simpan ke MongoDB
    try:
        from db import collection
        inserted = collection.insert_one(data)
    except Exception as e:
        print("MongoDB Error:", e)
    
    # Kirim ke Ubidots di background
    threading.Thread(target=send_to_ubidots_async, args=(data,)).start()
    
    return jsonify({"message": "Data diterima"}), 200  # Respon cepat ke ESP32

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"status": "ok", "message": "Server aktif!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5050)