from pymongo import MongoClient

class Database:
    def __init__(self, mongoUrl):
        self.db = MongoClient(mongoUrl)

    def getCollection(collection):
        return db[collection]
