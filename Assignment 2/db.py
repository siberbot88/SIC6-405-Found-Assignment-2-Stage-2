from pymongo import MongoClient

client = MongoClient("mongodb+srv://405Found-sic6:o4qL4fslJVAsoomm@405found.9ibtc.mongodb.net/?appName=405Found")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
db = client["MyDatabases"]  
collection = db["SensorData"]  