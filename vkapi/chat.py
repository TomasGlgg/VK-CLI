class Chat:
    id = None
    type = None
    title = None
    admin_id = None
    users = None
    push_settings = None
    photo_50 = None
    photo_100 = None
    photo_200 = None
    left = None
    kicked = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
