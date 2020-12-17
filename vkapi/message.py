from vkapi.attachments.audio import Audio
from vkapi.attachments.gift import Gift
from vkapi.attachments.link import Link
from vkapi.attachments.market import Market, MarketAlbum
from vkapi.comment import Comment
from vkapi.doc import Doc
from vkapi.attachments.photo import Photo
from vkapi.attachments.sticker import Sticker
from vkapi.geo import Geo
from vkapi.post import Post
from vkapi.user import User
from vkapi.attachments.video import Video


class Action:
    type = None
    member_id = None
    text = None
    email = None
    photo = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])



class Attachment:
    type = None
    photo = None
    video = None
    audio = None
    doc = None
    link = None
    market = None
    market_album = None
    wall = None
    wall_reply = None
    sticker = None
    gift = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        self.type = data['type']
        if self.type == "photo":
            self.photo = Photo(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "video":
            self.video = Video(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "audio":
            self.audio = Audio(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "doc":
            self.doc = Doc(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "link":
            self.link = Link(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "market":
            self.market = Market(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "market_album":
            self.market_album = MarketAlbum(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "wall":
            self.wall = Post(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "wall_reply":
            self.wall_reply = Comment(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "sticker":
            self.sticker = Sticker(v=self.v, api=self.api, data=data[self.type])
        elif self.type == "gift":
            self.gift = Gift(v=self.v, api=self.api, data=data[self.type])

    def getAttachment(self):
        if self.type == "photo":
            return self.photo
        elif self.type == "video":
            return self.video
        elif self.type == "audio":
            return self.audio
        elif self.type == "doc":
            return self.doc
        elif self.type == "link":
            return self.link
        elif self.type == "market":
            return self.market
        elif self.type == "market_album":
            return self.market_album
        elif self.type == "wall":
            return self.wall
        elif self.type == "wall_reply":
            return self.wall_reply
        elif self.type == "sticker":
            return self.sticker
        elif self.type == "gift":
            return self.gift

    def print(self):
        if self.type == "photo":
            self.photo.print()
        elif self.type == "video":
            self.video.print()
        # elif self.type == "audio":
        #     self.audio.print()
        # elif self.type == "doc":
        #     self.doc.print()
        # elif self.type == "link":
        #     self.link.print()
        # elif self.type == "market":
        #     self.market.print()
        # elif self.type == "market_album":
        #     self.market_album.print()
        # elif self.type == "wall":
        #     self.wall.print()
        # elif self.type == "wall_reply":
        #     self.wall_reply.print()
        elif self.type == "sticker":
            self.sticker.print()
        elif self.type == "gift":
            self.gift.print()


class Message:
    id = None
    date = None
    peer_id = None
    from_id = None
    text = None
    random_id = None
    ref = None
    ref_source = None
    attachments = None
    important = None
    geo = None
    payload = None
    keyboard = None
    fwd_messages = None
    reply_message = None
    action = None
    admin_author_id = None
    conversation_message_id = None
    is_cropped = None
    members_count = None
    update_time = None
    was_listened = None
    pinned_at = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "attachments":
                self.attachments = list()
                for item in data[key]:
                    attachment = Attachment(v=self.v, api=self.api, data=item)
                    self.attachments.append(attachment)
            elif key == "geo":
                self.geo = Geo(v=self.v, api=self.api, data=data[key])
            else:
                self.__setattr__(key, data[key])

    def getUserName(self):
        user = User(v=self.v, api=self.api, id=self.from_id)
        user.getUserInfo()
        return user.getName()
