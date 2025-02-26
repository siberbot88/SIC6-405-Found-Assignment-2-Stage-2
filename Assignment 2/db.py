from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin-405found:PNOJHpdexffLWupu@405found.9ibtc.mongodb.net/?retryWrites=true&w=majority&appName=405Found"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# client = MongoClient("mongodb+srv://405Found-sic6:PNOJHpdexffLWupu@405found.9ibtc.mongodb.net/?appName=405Found")

    
db = client["MyDatabases"]  
collection = db["SensorData"]  