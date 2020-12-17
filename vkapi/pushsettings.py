class PushSettings:
    disabled_until = None
    disabled_forever = None
    no_sound = None

    def __init__(self, v, api, data):
        for key in data.keys():
            self.__setattr__(key, data[key])
