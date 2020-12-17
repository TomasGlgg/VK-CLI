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
