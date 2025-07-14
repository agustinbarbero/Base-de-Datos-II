from pymongo import MongoClient

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient('localhost', 27017)
            cls._instance.db = cls._instance.client['eventos_db']
        return cls._instance

    def get_db(self):
        return self.db

    def close(self):
        self.client.close()
