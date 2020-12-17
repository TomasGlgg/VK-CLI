import requests

from consolephoto import show_image


class PhotoSize:
    url = None
    width = None
    height = None
    type = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Photo:
    id = None
    album_id = None
    owner_id = None
    user_id = None
    text = None
    data = None
    sizes = None
    width = None
    height = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "sizes":
                self.sizes = list()
                for item in data[key]:
                    photo_size = PhotoSize(v=self.v, api=self.api, data=item)
                    self.sizes.append(photo_size)
            else:
                self.__setattr__(key, data[key])

    def print(self):
        image = requests.get(self.sizes[0].url + '/', stream=True).raw
        show_image(image)
