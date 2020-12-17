class Country:
    _id = None
    title = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])
