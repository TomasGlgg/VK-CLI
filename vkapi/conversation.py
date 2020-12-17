from vkapi.geo import Geo
from vkapi.message import Message
from vkapi.pushsettings import PushSettings
from vkapi.user import User


class Peer:
    id = None
    type = None
    local_id = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class CanWrite:
    allowed = None
    reason = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            self.__setattr__(key, data[key])


class PinnedMessage:
    id = None
    date = None
    from_id = None
    text = None
    attachments = None
    geo = None
    fwd_messages = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "geo":
                self.geo = Geo(v=self.v, api=self.api, data=data[key])
            else:
                self.__setattr__(key, data[key])


class ChatSettings:
    members_count = None
    title = None
    pinned_message = None
    state = None
    photo = None
    active_ids = None
    is_group_channel = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "pinned_message":
                self.pinned_message = PinnedMessage(v=self.v, api=self.api, data=data[key])
            else:
                self.__setattr__(key, data[key])


class Conversation:
    peer = None
    in_read = None
    out_read = None
    unread_count = None
    important = None
    unanswered = None
    push_settings = None
    can_write = None
    chat_settings = None

    last_message = None

    def __init__(self, v, api, data):
        self.v = v
        self.api = api
        for key in data.keys():
            if key == "peer":
                self.peer = Peer(v=self.v, api=self.api, data=data[key])
            elif key == "push_settings":
                self.push_settings = PushSettings(v=self.v, api=self.api, data=data[key])
            elif key == "chat_settings":
                self.chat_settings = ChatSettings(v=self.v, api=self.api, data=data[key])
            else:
                self.__setattr__(key, data[key])

    def setLastMessage(self, data):
        self.last_message = Message(v=self.v, api=self.api, data=data)

    def getName(self):
        if self.peer.type == "user":
            user = User(v=self.v, api=self.api, id=self.peer.id)
            user.getUserInfo()
            return user.getName()
        elif self.peer.type == "chat":
            return self.chat_settings.title
        elif self.peer.type == "group":
            pass
        elif self.peer.type == "email":
            pass

    def getMessages(self, count=20):
        if count > 200:
            count = 200

        data = self.api.messages.getHistory(count=count, peer_id=self.peer.id, v=self.v)['items']

        messages = list()
        for item in data:
            messages.append(Message(v=self.v, api=self.api, data=item))
        return messages

    def print(self):
        print('-' * 40)
        print(f"""ID диалога: {self.peer.id}\nНазвание: {self.getName()}""")
        if self.peer.type == "user" or self.peer.type == "chat":
            message_username = self.last_message.getUserName()
            print(f"""[{message_username}]: {self.last_message.text}""")
            for attach in self.last_message.attachments:
                print(attach.type)
                attach.print()
