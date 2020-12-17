class Link:
    url = None
    title = None
    caption = None
    description = None
    photo = None
    product = None
    button = None
    preview_page = None
    preview_url = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])

