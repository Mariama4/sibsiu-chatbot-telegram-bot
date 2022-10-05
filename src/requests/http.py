import requests
import os


class Http:
    def __init__(self):
        self._api_url = os.getenv('API_URL')
        self._headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'X-Powered-By': 'Express',
            'Accept': 'application/json',
            'bot_token': os.getenv('API_BOT_TOKEN')
        }

    def get(self, path, json=None):
        response = requests.get(
            url=self._api_url + path,
            headers=self._headers,
            json=json
        )
        return response.json()

    def post(self, path, json=None):
        response = requests.post(
            url=self._api_url + path,
            headers=self._headers,
            json=json
        )
        return response.json()

    def patch(self, path, json=None):
        response = requests.patch(
            url=self._api_url + path,
            headers=self._headers,
            json=json
        )
        return response.json()
