class Coordinate:
    latitude = None
    longitude = None


class Place:
    _id = None
    title = None
    latitude = None
    longitude = None
    created = None
    icon = None
    country = None
    city = None


class Geo:
    type = None
    coordinates = None
    place = None
    showmap = None

    def __init__(self, v, api, data):
        for key in data.keys():
            self.__setattr__(key, data[key])
