from datetime import datetime
from termcolor import colored


def _print_private_message(message):
    date = datetime.fromtimestamp(message['date'])
    print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
    if message['from_id'] != message['peer_id']:
        print('Message', colored('(Вы):', 'green'), message['text'])
    else:
        print('Message:', message['text'])
    if len(message['attachments']):
        print('Дополнительно:', end=' ')
        for attachment in message['attachments']:
            print(colored(attachment['type'], 'cyan'), end=' ')
        print()


class Private_messages_parser:
    def __init__(self, api, peer_id):
        self.peer_id = peer_id
        self.api = api

    def print_last_messages(self, count):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=5.126)['items']
        for message in messages[::-1]:
            _print_private_message(message)


class Chat_messages_parser:
    def __init__(self, api, chat_id, profile_id):
        self.peer_id = chat_id
        self.api = api
        self.profile_id = profile_id

    def _print_chat_message(self, message):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['from_id'] == self.profile_id['id']:
            print('Сообщение', colored('(Вы):', 'green'), end=' ')
        else:
            peer_info = self.api.users.get(user_ids=[message['from_id']], v=5.126, name_case='gen')[0]
            print('Сообщение от', colored(peer_info['first_name'] + ' ' + peer_info['last_name'], 'red') + ':', end=' ')
        print(message['text'])

    def print_last_messages(self, count):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=5.126)['items']
        for message in messages[::-1]:
            self._print_chat_message(message)
