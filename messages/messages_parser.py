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
    def __init__(self, api, chat_id):
        self.peer_id = chat_id
        self.api = api

    def print_last_messages(self, count):
        pass
