from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hackmate"]

users = db.users
requests = db.requests
notifications = db.notifications