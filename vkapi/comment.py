class Thread:
    count = None
    items = None
    can_post = None
    show_reply_button = None
    groups_can_post = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Comment:
    id = None
    from_id = None
    date = None
    text = None
    donut = None
    reply_to_user = None
    reply_to_comment = None
    attachments = None
    parents_stack = None
    thread = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
