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
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    motion = data.get("motion")  

    if temperature is None or humidity is None or motion is None:
        return jsonify({"error": "Data tidak lengkap"}), 400

    new_data = {
        "temperature": temperature,
        "humidity": humidity,
        "motion": motion  
    }
    inserted_id = collection.insert_one(new_data).inserted_id  

    
    ubidots_payload = {
        "temperature": temperature,
        "humidity": humidity,
        "motion": motion  
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": UBIDOTS_TOKEN
    }

    response = requests.post(UBIDOTS_URL, json=ubidots_payload, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        return jsonify({"message": "Data terkirim Ubidots"}), 200
    else:
        return jsonify({"message": "Data gagal terkirim ke Ubidots", "error": response.text}), 500


@app.route('/sensor1', methods=['GET'])
def get_all_data():
    all_data = collection.find()  
    result = []

    for data in all_data:
        result.append({
            "id": str(data["_id"]),
            "temperature": data.get("temperature", "N/A"),  
            "humidity": data.get("humidity", "N/A"),
            "motion": data.get("motion", "N/A")  
        })

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

