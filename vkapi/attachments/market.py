class MarketAlbum:
    id = None
    owner_id = None
    title = None
    photo = None
    count = None
    updated_time = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Market:
    id = None
    owner_id = None
    title = None
    description = None
    price = None
    dimension = None
    weight = None
    category = None
    thumb_photo = None
    date = None
    availability = None
    is_favorite = None
    sku = None

    photos = None
    can_comment = None
    can_repost = None
    likes = None
    url = None
    button_title = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
