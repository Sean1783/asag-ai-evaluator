import os
from typing import Any, List

from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.synchronous.cursor import Cursor, Mapping

from constants import DbDetails

class DatabaseManager:
    def __init__(self, database_name: str) -> None:
        self.db = None
        self.connect_to_database(database_name)
        self.collection = None

    def set_collection(self, collection_name: str) -> None:
        self.collection = collection_name

    def connect_to_database(self, db_name : str) -> None:
        load_dotenv()
        uri = os.getenv("MONGO_URI")
        try:
            client = MongoClient(uri, tls=True, tlsCAFile='/etc/ssl/cert.pem')
            self.db = client[db_name]
        except Exception as e:
            print(f"Database did not connect successfully : {e}")

    def insert_document(self, collection, document) -> int | None:
        try:
            collection = self.db[collection]
            result = collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f"Database did not insert document successfully : {e}")

    # def insert_documents(self, documents: List, collection_name: str = None) -> List | None:
    def insert_documents(self, documents : List) -> List | None:
        try:
            # if collection_name is None:
            collection = self.db[self.collection]
            # else:
            #     collection = self.db[collection_name]
            result = collection.insert_many(documents)
            return result.inserted_ids
        except Exception as e:
            print(f"Database did not insert documents successfully : {e}")

    def find_documents(self, collection, query=None) -> Cursor[Mapping[str, Any] | Any] | None:
        if query is None:
            query = {}
        try:
            collection = self.db[collection]
            results = collection.find({query})
            return results
        except Exception as e:
            print(f"Database did not find documents successfully : {e}")
