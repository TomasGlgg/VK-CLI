class Peer:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.local_id = data['local_id']

class Photo:
    def __init__(self, data):
        self.photo_50 = data['photo_50']
        self.photo_100 = data['photo_100']
        self.photo_200 = data['photo_200']


class Chat_settings:
    def __init__(self, api, data):
        self.members_count = data['members_count']
        self.title = data['title']
        self.state = data['state']
        self.photo = Photo(data['photo'])
        self.active_ids = data['active_ids']


class User:
    def __init__(self, data):
        self.id = data['id']
        self.firs_name = data['first_name']
        self.last_name = data['last_name']


class Conversation:
    def __init__(self, api, data):
        self.api = api
        self.peer = Peer(data['peer'])
        self.in_read = data['in_read']
        self.out_read = data['out_read']
        self.important = data['important']
        if self.peer.type == "chat":
            self.chat_settings = Chat_settings(api, data['chat_settings'])

    def getName(self):
        if self.peer.type == "user":
            data = self.api.users.get(user_ids=[self.peer.id], v='5.52')[0]
            user = User(data)
            name = user.firs_name + ' ' + user.last_name
            return name
        elif self.peer.type == "chat":
            return self.chat_settings.title
        elif self.peer.type == "group":
            pass
        elif self.peer.type == "email":
            pass

    def print(self):
        print(f"""ID диалога: {self.peer.id}\nНазвание: {self.getName()}""")


class Last_message:
    def __init__(self, api, data):
        self.api = api
        self.id = data['id']
        self.date = data['date']
        self.peer_id = data['peer_id']
        self.from_id = data['from_id']
        self.text = data['text']

    def getNameFrom(self):
        data = self.api.users.get(user_ids=[self.from_id], v='5.52')[0]
        user = User(data)
        return user.firs_name + ' ' + user.last_name

    def print(self):
        print(f"""Последнее сообщение: ({self.getNameFrom()}) {self.text}""")


class Message:
    def __init__(self, api, data):
        self.conversation = Conversation(api, data['conversation'])
        self.last_message = Last_message(api, data['last_message'])

    def print(self):
        print("-" * 40)
        self.conversation.print()
        self.last_message.print()
