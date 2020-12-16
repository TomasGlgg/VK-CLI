class Peer:
    def __init__(self, api, data):
        self.id = data['id']
        self.type = data['type']
        self.local_id = data['local_id']


class Push_settings:
    def __init__(self, api, data):
        if data is None:
            return
        for key in ["disabled_until", "disabled_forever", "no_sound"]:
            if key not in data.keys():
                data[key] = None
        self.disabled_until = data['disabled_until']
        self.disabled_forever = data['disabled_forever']
        self.no_sound = data['no_sound']


class Can_write:
    def __init__(self, api, data):
        for key in ["allowed", "reason"]:
            if key not in data.keys():
                data[key] = None
        self.allowed = data['allowed']
        self.reason = data['reason']

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
        if data is None:
            return
        for key in ["members_count", "title", "pinned_message", "state", "photo", "active_ids", "is_group_channel"]:
            if key not in data.keys():
                data[key] = None
        self.members_count = data['members_count']
        self.title = data['title']
        self.pinned_message = data['pinned_message']
        self.state = data['state']
        self.photo = Photo(api, data['photo'])
        self.active_ids = data['active_ids']
        self.is_group_channel = data['is_group_channel']


class User:
    def __init__(self, api, data):
        if data is None:
            return
        for key in ["id", "first_name", "last_name", "deactivated", "is_closed", "can_access_closed"]:
            if key not in data.keys():
                data[key] = None
        self.id = data['id']
        self.firs_name = data['first_name']
        self.last_name = data['last_name']
        self.deactivated = data['deactivated']
        self.is_closed = data['is_closed']
        self.can_access_closed = data['can_access_closed']


class Conversation:
    def __init__(self, api, data):
        self.api = api
        for key in ["peer", "in_read", "out_read", "unread_count", "important", "unanswered", "push_settings",
                    "can_write", "chat_settings"]:
            if key not in data.keys():
                data[key] = None
        self.peer = Peer(api, data['peer'])
        self.in_read = data['in_read']
        self.out_read = data['out_read']
        self.unread_count = data['unread_count']
        self.important = data['important']
        self.unanswered = data['unanswered']
        self.push_settings = Push_settings(api, data['push_settings'])
        self.can_write = Can_write(api, data['can_write'])
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


class Parser:
    def __init__(self, api):
        self.api = api

    def show_user_chat(self, data):
        peer_id = data['conversation']['peer']['id']
        user = self.api.users.get(user_ids=[peer_id], v='5.52')[0]
        print('Peer: ({})'.format(peer_id), user['first_name'], user['last_name'])
        if len(data['last_message']['attachments']):
            print('Type:', data['last_message']['attachments'][0]['type'])
        if data['last_message']['from_id'] != peer_id:
            print('Message (Вы):')
        else:
            print('Message:')
        print(data['last_message']['text'])

    def show_chat_chat(self, data):
        # print(json.dumps(data, indent=8, sort_keys=True))
        title = data['conversation']['chat_settings']['title']
        last_peer = data['last_message']['from_id']
        if last_peer < 0:
            return
        print('Chat:', title)
        user = self.api.users.get(user_ids=[last_peer], v='5.52')[0]
        print('Peer:', user['first_name'], user['last_name'])
        if len(data['last_message']['attachments']):
            print('Other:', end=' ')
            for other in data['last_message']['attachments']:
                print(other['type'], end=' ')
            print()
        print('Message:', data['last_message']['text'])

    def show_message(self, data):
        # print(json.dumps(data, indent=8, sort_keys=True))
        if data['conversation']['peer']['type'] == 'user':
            self.show_user_chat(data)
        elif data['conversation']['peer']['type'] == 'chat':
            self.show_chat_chat(data)
        else:
            print('Peer', data['conversation']['peer']['type'], 'is not recognized')
