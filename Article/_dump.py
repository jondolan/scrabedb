from pymongo import MongoClient
from datetime import datetime

def dump_collection(collection):
    print(collection.find())