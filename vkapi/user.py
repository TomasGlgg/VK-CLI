from vkapi.city import City
from vkapi.country import Country


class Contacts:
    mobile_phone = None
    home_phone = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])


class Crop:
    x = None
    y = None
    x2 = None
    y2 = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])


class Rect:
    x = None
    y = None
    x2 = None
    y2 = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])


class CropPhoto:
    photo = None
    crop = None
    rect = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Career:
    group_id = None
    company = None
    country_id = None
    city_id = None
    city_name = None
    _from = None
    until = None
    position = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "from":
                self._from = data[key]
            else:
                self.__setattr__(key, data[key])


class LastSeen:
    time = None
    platform = None

    def __init__(self, data):
        for key in data.keys():
            self.__setattr__(key, data[key])


class Military:
    unit = None
    unit_id = None
    country_id = None
    _from = None
    until = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "from":
                self._from = data[key]
            else:
                self.__setattr__(key, data[key])


class Occupation:
    type = None
    id = None
    name = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Personal:
    political = None
    langs = None
    religion = None
    inspired_by = None
    people_main = None
    life_main = None
    smoking = None
    alcohol = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class Relative:
    id = None
    name = None
    type = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class School:
    id = None
    country = None
    city = None
    name = None
    year_from = None
    year_to = None
    year_graduated = None
    _class = None
    speciality = None
    type = None
    type_str = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "class":
                self._class = data[key]
            else:
                self.__setattr__(key, data[key])


class University:
    id = None
    country = None
    city = None
    name = None
    faculty = None
    faculty_name = None
    chair = None
    chair_name = None
    graduation = None
    education_form = None
    education_status = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class User:
    # Основные поля
    id = None
    first_name = None
    last_name = None
    deactivated = None
    is_closed = None
    can_access_closed = None

    # Дополнительные
    about = None
    activities = None
    bdate = None
    blacklisted = None
    blacklisted_by_me = None
    books = None
    can_post = None
    can_see_all_posts = None
    can_see_audio = None
    can_send_friend_request = None
    can_write_private_message = None
    career = None
    city = None
    common_count = None
    connections = None
    contacts = None
    counters = None
    country = None
    crop_photo = None
    domain = None
    education = None
    exports = None
    first_name_case = None
    followers_count = None
    friend_status = None
    games = None
    has_mobile = None
    has_photo = None
    home_town = None
    interests = None
    is_favorite = None
    is_friend = None
    is_hidden_from_feed = None
    last_name_case = None
    last_seen = None
    lists = None

    maiden_name = None
    military = None
    movies = None
    music = None
    nickname = None
    occupation = None
    online = None
    personal = None
    photo_50 = None
    photo_100 = None
    photo_200_orig = None
    photo_200 = None
    photo_400_orig = None
    photo_id = None
    photo_max = None
    photo_max_orig = None
    quotes = None
    relatives = None
    relation = None
    schools = None
    screen_name = None
    sex = None
    site = None
    status = None
    timezone = None
    trending = None
    tv = None
    universities = None
    verified = None
    wall_default = None

    def __init__(self, v, api, id=None):
        self.api = api
        self.v = v
        self.id = id

    def getUserInfo(self):
        fields = ["photo_id", "verified", "sex", "bdate", "city", "country", "home_town", "has_photo", "photo_50",
                  "photo_100", "photo_200_orig", "photo_200", "photo_400_orig", "photo_max", "photo_max_orig", "online",
                  "domain", "has_mobile", "contacts", "site", "education", "universities", "schools", "status",
                  "last_seen", "followers_count", "common_count", "occupation", "nickname", "relatives", "relation",
                  "personal", "connections", "exports", "activities", "interests", "music", "movies", "tv", "books",
                  "games", "about", "quotes", "can_post", "can_see_all_posts", "can_see_audio",
                  "can_write_private_message", "can_send_friend_request", "is_favorite", "is_hidden_from_feed",
                  "timezone", "screen_name", "maiden_name", "crop_photo", "is_friend", "friend_status", "career",
                  "military", "blacklisted", "blacklisted_by_me", "can_be_invited_group"]

        if self.id is None:
            data = self.api.users.get(fields=fields, v=self.v)[0]
        else:
            data = self.api.users.get(user_ids=[self.id], fields=fields, v=self.v)[0]

        for key in data.keys():
            if key == "career":
                self.career = list()
                for item in data[key]:
                    self.career.append(Career(v=self.v, api=self.api, data=item))
            elif key == "city":
                self.city = City(v=self.v, api=self.api, data=data[key])
            elif key == "country":
                self.country = Country(v=self.v, api=self.api, data=data[key])
            elif key == "crop_photo":
                self.crop_photo = CropPhoto(v=self.v, api=self.api, data=data[key])
            elif key == "military":
                self.military = list()
                for item in data[key]:
                    self.military.append(Military(v=self.v, api=self.api, data=item))
            elif key == "occupation":
                self.occupation = Occupation(v=self.v, api=self.api, data=data[key])
            elif key == "personal":
                self.personal = Personal(v=self.v, api=self.api, data=data[key])
            elif key == "relatives":
                self.relatives = list()
                for item in data[key]:
                    self.relatives.append(Relative(v=self.v, api=self.api, data=item))
            elif key == "school":
                self.schools = list()
                for item in data[key]:
                    self.schools.append(School(v=self.v, api=self.api, data=item))
            elif key == "universities":
                self.universities = list()
                for item in data[key]:
                    self.universities.append(University(v=self.v, api=self.api, data=item))
            else:
                self.__setattr__(key, data[key])

    def getName(self):
        return self.first_name + ' ' + self.last_name
