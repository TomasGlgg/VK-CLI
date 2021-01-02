from datetime import datetime
from termcolor import colored


class Private_messages_parser:
    def __init__(self, api, peer_id):
        self.peer_id = peer_id
        self.api = api

    @staticmethod
    def _print_private_message(message):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['user_id'] != message['from_id']:
            print('Message', colored('(Вы):', 'green'), message['body'])
        else:
            print('Message:', message['body'])
        if 'attachments' in message:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, return_unread_messages_ids=False):
        unread_messages_ids = []
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=5.52)['items']
        for message in messages[::-1]:
            self._print_private_message(message)
            if message['read_state'] == 0 and return_unread_messages_ids:
                unread_messages_ids.append(message['id'])
        if return_unread_messages_ids:
            return unread_messages_ids


class Chat_messages_parser:
    def __init__(self, api, chat_id, profile_id):
        self.peer_id = chat_id
        self.api = api
        self.profile_id = profile_id

    def _print_last_message(self, message):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['from_id'] == self.profile_id['id']:
            print('Сообщение', colored('(Вы):', 'green'), end=' ')
        else:
            peer_info = self.api.users.get(user_ids=[message['from_id']], v=5.52, name_case='gen')[0]
            print('Сообщение от', colored(peer_info['first_name'] + ' ' + peer_info['last_name'], 'red') + ':', end=' ')
        print(message['body'])

    def print_last_messages(self, count, return_unread_messages_ids=False):
        unread_messages_ids = []
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=5.52)['items']
        for message in messages[::-1]:
            self._print_last_message(message)
            if message['read_state'] == 0 and return_unread_messages_ids:
                unread_messages_ids.append(message['id'])
        if return_unread_messages_ids:
            return unread_messages_ids


class Group_messages_parser:
    def __init__(self, api, group_id):
        self.api = api
        self.group_id = group_id

    @staticmethod
    def _print_last_message(message):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['user_id'] != message['from_id']:
            print('Message', colored('(Вы):', 'green'), message['body'])
        else:
            print('Message:', message['body'])
        if 'attachments' in message:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, return_unread_messages_ids=False):
        unread_messages_ids = []
        messages = self.api.messages.getHistory(peer_id=self.group_id, count=count, v=5.52)['items']
        for message in messages[::-1]:
            self._print_last_message(message)
            if message['read_state'] == 0 and return_unread_messages_ids:
                unread_messages_ids.append(message['id'])
        if return_unread_messages_ids:
            return unread_messages_ids
