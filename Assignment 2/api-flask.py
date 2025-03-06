from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from db import collection
import requests

app = Flask(__name__)

UBIDOTS_TOKEN = "BBUS-KBGoN2Efxyadt5RaZLzKhMiSR4zxqU"
UBIDOTS_DEVICE_LABEL = "v1.6/devices/si6-405-found/"
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/si6-405-found/"


@app.route('/sensor1', methods=['POST'])
def receive_sensor_data():
    data = request.json
    required_fields = ["temperature", "humidity", "motion", "ldr", "status"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Data untuk MongoDB
    new_data = {
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "motion": data["motion"],
        "ldr": data["ldr"],
        "status": data["status"]
    }
    
    # Data untuk Ubidots (tanpa status)
    ubidots_payload = {
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "motion": data["motion"],
        "ldr": data["ldr"]
    }
    
    # Simpan ke MongoDB
    try:
        collection.insert_one(new_data)
    except Exception as e:
        print("Error MongoDB:", e)
    
    # Kirim ke Ubidots
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    try:
        response = requests.post(UBIDOTS_URL, json=ubidots_payload, headers=headers)
        if response.status_code in [200, 201]:
            return jsonify({"message": "Data terkirim ke semua sistem"}), 200
        else:
            return jsonify({"error": "Gagal ke Ubidots", "detail": response.text}), 500
    except Exception as e:
        return jsonify({"error": "Koneksi Ubidots gagal", "detail": str(e)}), 500

@app.route('/sensor1', methods=['GET'])
def get_all_data():
    all_data = collection.find()
    result = []
    
    for doc in all_data:
        doc_data = {
            "id": str(doc["_id"]),
            "temperature": doc.get("temperature", "N/A"),
            "humidity": doc.get("humidity", "N/A"),
            "motion": doc.get("motion", "N/A"),
            "ldr": doc.get("ldr", "N/A")
        }
        result.append(doc_data)
    
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")