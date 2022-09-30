import json

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

    def setStatus(self, status):
        self._status = status

    def updateStatus(self, url):
        response = self._database.patch(
            url=self._url + url,
            json={'id': f'{self._id}',
                  'status': f'{self._status}'}
        )
        print(response)


