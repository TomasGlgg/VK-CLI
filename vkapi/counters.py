class Counters:
    albums = None
    videos = None
    audios = None
    photos = None
    notes = None
    friends = None
    groups = None
    online_friends = None
    mutual_friends = None
    user_videos = None
    followers = None
    pages = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])
