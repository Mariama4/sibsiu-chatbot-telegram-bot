class Frame:

    frames = {}

    def __init__(self, frame):
        self._frame = frame
        self.__parseFrames__(frame)

    def __parseFrames__(self, data):
        frames = data['frames']
        # NEW
        # frames = data['data']
        for index, value in enumerate(frames):
            frame = value['data']
            self.frames[frame['ID']] = frame['DATA']

    def getIdOfFrames(self):
        return list(self.frames.keys())
