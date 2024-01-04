import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set.")

        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client["Authorized_user"]
        self.collection = self.db["my_table"]
