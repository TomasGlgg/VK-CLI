class Preview:
    photo = None
    graffiti = None
    audio_message = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Doc:
    id = None
    owner_id = None
    title = None
    size = None
    ext = None
    url = None
    date = None
    type = None
    preview = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
