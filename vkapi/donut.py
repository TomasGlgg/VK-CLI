class Donut:
    is_don = None
    placeholder = None

    paid_duration = None
    can_publish_free_copy = None
    edit_mode = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
