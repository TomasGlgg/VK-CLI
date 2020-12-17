class PhotoSize:
    url = None
    width = None
    height = None
    type = None


class Photo:
    _id = None
    album_id = None
    owner_id = None
    user_id = None
    text = None
    data = None
    sizes = None
    width = None
    height = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])
