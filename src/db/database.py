import pymongo


class Database:
    def __init__(self):
        self._client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._db = self._client['telegram_bot']
        self._configuration = self._db['configuration']
