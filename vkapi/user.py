class Contacts:
    mobile_phone = None
    home_phone = None


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


class Crop:
    x = None
    y = None
    x2 = None
    y2 = None


class CropPhoto:
    photo = None
    crop = None
    rect = None


class Career:
    group_id = None
    company = None
    country_id = None
    city_id = None
    city_name = None
    _from = None
    until = None
    position = None


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
