from pymongo import MongoClient

client = MongoClient("mongodb+srv://sic6-405Found:XKsdbzPxxosoP00a@405foundsic6.rllhr.mongodb.net/?retryWrites=true&w=majority&appName=405FoundSIC6")
db = client["MyDatabases"]
collection = db["SensorData"]