import pymongo

class DBHelper:

    def __init__(self, dbname="test"):
        self.dbname = dbname
        mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
        db = mongo_client.dbname
        return db
