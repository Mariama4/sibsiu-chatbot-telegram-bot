import requests


class Database:
    def __init__(self, url, login, password):
        self._url = url
        self._auth = {
            'email': login,
            'password': password
        }
        self._headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'X-Powered-By': 'Express',
            'Accept': 'application/json'
        }

    def login(self, url):
        response = requests.post(
            url=self._url + url,
            headers=self._headers,
            json=self._auth
        )
        token = response.json()['token']
        self._headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'X-Powered-By': 'Express',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        return "Success!"

    def get(self, url, json=None):
        response = requests.get(
            url=self._url + url,
            headers=self._headers,
            json=json
        )
        return response.json()

    def post(self, url, json=None):
        response = requests.post(
            url=self._url + url,
            headers=self._headers,
            json=json
        )
        return response.json()

    def patch(self, url, json=None):
        response = requests.patch(
            url=self._url + url,
            headers=self._headers,
            json=json
        )
        return response.json()
