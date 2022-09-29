from dotenv import load_dotenv
import os
load_dotenv()


class Frame:

    frames = {}

    def __init__(self, database):
        self._database = database

    def __parseFrames__(self, data):
        frames = data['frames']
        for index, value in enumerate(frames):
            frame = value['data']
            self.frames[frame['ID']] = frame['DATA']

    def getFrames(self):
        response = self._database.get(
            url=os.getenv('API_URL_FRAME')
        )
        self.__parseFrames__(response)

    def getIdOfFrames(self):
        return self.frames.keys()
