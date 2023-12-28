# database.py
import pymongo

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Authorized_user"]
        self.collection = self.db["my_table"]
