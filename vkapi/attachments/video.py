class Video:
    id = None
    owner_id = None
    title = None
    description = None
    duration = None
    image = None
    first_frame = None
    date = None
    adding_date = None
    views = None
    local_views = None
    comments = None
    player = None
    platform = None
    can_edit = None
    can_add = None
    is_private = None
    access_key = None
    processing = None
    is_favorite = None
    can_comment = None
    can_like = None
    can_repost = None
    can_subscribe = None
    can_add_to_faves = None
    can_attach_link = None
    width = None
    height = None
    user_id = None
    converting = None
    added = None
    is_subscribed = None
    repeat = None
    type = None
    balance = None
    live_status = None
    live = None
    upcoming = None
    spectators = None
    likes = None
    reposts = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])

    def print(self):
        pass