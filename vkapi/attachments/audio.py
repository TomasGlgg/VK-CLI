class Audio:
    id = None
    owner_id = None
    artist = None
    title = None
    duration = None
    url = None
    lyrics_id = None
    album_id = None
    genre_id = None
    date = None
    no_search = None
    is_hq = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
