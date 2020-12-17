class Gift:
    id = None
    thumb_256 = None
    thumb_96 = None
    thumb_48 = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])

    def print(self):
        pass