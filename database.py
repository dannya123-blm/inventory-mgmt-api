from pymongo import MongoClient
MONGO_URL = "mongodb+srv://admin11:adminpass11@inventory-management-db.ue0pccy.mongodb.net/inventoryDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client["inventoryDB"]
products_collection = db["products"]