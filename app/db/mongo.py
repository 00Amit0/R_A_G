from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List
from app.config import settings


client = None

def get_client():
    global client
    if client is None:
        client = MongoClient(settings.mongo_uri)
    return client

def get_db():
    return get_client()[settings.mongo_db]

def get_collection(name='documents'):
    return get_db()[name]

def insert_chunk(chunk: dict):
    col = get_collection()
    return col.insert_one(chunk)

def fetch_all_docs():
    col = get_collection()
    return list(col.find({}))

def ensure_vector_index():
    # If you want to use MongoDB Atlas Vector Search create index via Atlas console.
    # For local MongoDB, there's no built-in vector index (unless using enterprise features).
    # Keep a placeholder here.
    pass