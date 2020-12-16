class Peer:
    def __init__(self, api, data):
        self.id = data['id']
        self.type = data['type']
        self.local_id = data['local_id']


class Push_settings:
    def __init__(self, api, data):
        self.disabled_forever = data['disabled_forever']
        self.no_sound = data['no_sound']


class Can_write:
    def __init__(self, api, data):
        self.allowed = data['allowed']

    def check(self):
        if not self.allowed:
            if self.reason == '18':
                return "пользователь заблокирован или удален"
            elif self.reason == '900':
                return "нельзя отправить сообщение пользователю, который в чёрном списке"
            elif self.reason == '901':
                return "пользователь запретил сообщения от сообщества"
            elif self.reason == '902':
                return "пользователь запретил присылать ему сообщения с помощью настроек приватности"
            elif self.reason == '915':
                return "в сообществе заблокированы сообщения"
            elif self.reason == '917':
                return "нет доступа к чату"
            elif self.reason == '918':
                return "нет доступа к e-mail"
            elif self.reason == '203':
                return "нет доступа к сообществу"


class Photo:
    def __init__(self, api, data):
        self.photo_50 = data['photo_50']
        self.photo_100 = data['photo_100']
        self.photo_200 = data['photo_200']


class Chat_settings:
    def __init__(self, api, data):
        self.members_count = data['members_count']
        self.title = data['title']
        self.pinned_message = data['pinned_message']
        self.state = data['state']
        self.photo = Photo(api, data['photo'])
        self.active_ids = data['active_ids']


class User:
    def __init__(self, api, data):
        self.id = data['id']
        self.firs_name = data['first_name']
        self.last_name = data['last_name']


class Conversation:
    def __init__(self, api, data):
        self.api = api
        self.peer = Peer(api, data['peer'])
        self.in_read = data['in_read']
        self.out_read = data['out_read']
        self.important = data['important']
        self.can_write = Can_write(api, data['can_write'])
        if self.peer.type == "chat":
            self.push_settings = Push_settings(api, data['push_settings'])
            self.chat_settings = Chat_settings(api, data['chat_settings'])

    def getName(self):
        if self.peer.type == "user":
            data = self.api.users.get(user_ids=[self.peer.id], v='5.52')[0]
            user = User(self.api, data)
            name = user.firs_name + ' ' + user.last_name
            return name
        elif self.peer.type == "chat":
            return self.chat_settings.title
        elif self.peer.type == "group":
            pass
        elif self.peer.type == "email":
            pass

    def print(self):
        print("Название: ", self.getName())


class Last_message:
    def __init__(self, api, data):
        self.id = data['id']
        self.date = data['date']
        self.peer_id = data['peer_id']
        self.from_id = data['from_id']
        self.text = data['text']

    def print(self):
        print("Последнее сообщение: ", self.text)


class Message:
    def __init__(self, api, data):
        self.conversation = Conversation(api, data['conversation'])
        self.last_message = Last_message(api, data['last_message'])

    def print(self):
        print("-" * 20)
        self.conversation.print()
        self.last_message.print()
        print("-" * 20)
