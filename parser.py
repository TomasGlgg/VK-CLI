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


class Country:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']


class User:
    def __init__(self, data):
        self.id = data['id']
        self.firs_name = data['first_name']
        self.last_name = data['last_name']
        if 'screen_name' in data.keys():
            self.screen_name = data['screen_name']
            self.bdate = data['bdate']
            self.phone = data['phone']
            self.country = Country(data['country'])
            self.status = data['status']


class Message_1:
    def __init__(self, api, data):
        self.api = api
        self.date = data['date']
        self.from_id = data['from_id']
        self.id = data['id']
        self.out = data['out']
        # self.peer_id = data['peer_id']
        if 'text' not in data.keys():
            self.text = data['body']
        else:
            self.text = data['text']
            self.conversation_message_id = data['conversation_message_id']
            self.fwd_messages = data['fwd_messages']
            self.important = data['important']
            self.random_id = data['random_id']
            self.attachments = data['attachments']
            self.is_hidden = data['is_hidden']

    def getUserName(self):
        data = self.api.users.get(user_ids=[self.from_id], v='5.126')[0]
        user = User(data)
        return user.firs_name + ' ' + user.last_name

    def print(self):
        print(f"""{self.getUserName()}: {self.text}""")


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

    def getMessages(self, count):
        if count is None:
            count = 20
        if count > 200:
            count = 200
        data = self.api.messages.getHistory(count=count, peer_id=self.peer.id, v='5.52')['items']
        messages = list()
        for item in data:
            messages.append(Message_1(self.api, item))
        return messages

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
        if self.conversation.peer.type != "group":
            self.last_message.print()
