import os
import pymongo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        # Get the MongoDB connection string from the environment variable
        mongo_uri = os.getenv("MONGO_URI")

        # Check if the environment variable is set
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set.")

        # Connect to MongoDB using the provided connection string
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client["Authorized_user"]
        self.collection = self.db["my_table"]
