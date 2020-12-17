class Image:
    url = None
    width = None
    height = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Sticker:
    product_id = None
    sticker_id = None
    images = None
    images_with_background = None
    animation_url = None
    is_allowed = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])

    def print(self):
        pass