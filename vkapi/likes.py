class Likes:
    count = None
    user_likes = None
    can_like = None
    can_publish = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])