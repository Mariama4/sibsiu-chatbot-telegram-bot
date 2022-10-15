class HttpLogger:
    def __init__(self, api, url_log, url_tgbot_user, url_frame_log):
        self._api = api
        self._url_log = url_log
        self._url_tgbot_user = url_tgbot_user
        self._url_frame_log = url_frame_log

    async def checkUser(self, message):
        user = {
            'id': message['from']['id'],
            'is_bot': message['from']['is_bot'],
            'first_name': message['from']['first_name'],
            'last_name': message['from']['last_name'],
            'username': message['from']['username'],
            'language_code': message['from']['language_code'],
        }
        await self._api.asyncPost(path=self._url_tgbot_user, json=user)

    async def sendAction(self, message):
        data = {
            'data': str(message)
        }
        await self._api.asyncPost(path=self._url_log, json=data)

    async def sendFrameAction(self, message, frame_id):
        data = {
            'user_id': message['from']['id'],
            'frame_id': frame_id
        }
        await self._api.asyncPost(path=self._url_frame_log, json=data)
