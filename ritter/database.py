from pymongo import MongoClient


class DatabaseMixin:
    def __init__(self, db, collection):
        self.db = db
