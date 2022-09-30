class Config:
    def __init__(self, database, url):
        self._database = database
        self._url = url
        response = database.get(url)
        self._id = response['configuration'][0]['id']
        self._token = response['configuration'][0]['token']
        self._status = response['configuration'][0]['status']
        self._bot_name = response['configuration'][0]['bot_name']

    def getToken(self):
        return self._token


