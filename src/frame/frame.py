class Frame:

    frames = {}

    def __init__(self, frame):
        self._frame = frame
        self.__parseFrames__(frame)

    def __parseFrames__(self, data):
        frames = data['result']

        for index, value in enumerate(frames):
            frame = value['data']
            self.frames[frame['frame_id']] = frame['frame']

    def getIdOfFrames(self):
        return list(self.frames.keys())
