class Reposts:
    count = None
    user_reposted = None
    wall_count = None
    mail_count = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])
