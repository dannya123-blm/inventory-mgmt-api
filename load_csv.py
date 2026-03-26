import pandas as pd
from pymongo import MongoClient
MONGO_URL = "mongodb+srv://admin11:adminpass11@inventory-management-db.ue0pccy.mongodb.net/inventoryDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client["inventoryDB"]
collection = db["products"]
df = pd.read_csv("products.csv")
data = df.to_dict(orient="records")
collection.insert_many(data)
print("CSV uploaded successfully")