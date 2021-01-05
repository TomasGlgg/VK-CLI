from datetime import datetime
from termcolor import colored


class Private_messages_parser:
    def __init__(self, api, peer_id):
        self.peer_id = peer_id
        self.api = api

    @staticmethod
    def _print_private_message(message):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if message['text']:
            if message['out']:
                print('Сообщение', colored('(Вы):', 'green'), message['text'])
            else:
                print('Сообщение', colored('(Собеседник):', 'blue'), message['text'])
        if message['attachments']:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, extended=True,
                                                v=self.api.VK_API_VERSION)
        for message in messages['items'][::-1]:
            self._print_private_message(message)
        if mark_unreads_messages:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True,
                                         v=self.api.VK_API_VERSION)


class Chat_messages_parser:
    def __init__(self, api, chat_id, profile_id):
        self.peer_id = chat_id
        self.api = api
        self.profile_id = profile_id

    def _print_last_message(self, message):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if message['text']:
            if message['out']:
                print('Сообщение', colored('(Вы):', 'green'), end=' ')
            else:
                peer_info = self.api.users.get(user_ids=[message['from_id']], v=self.api.VK_API_VERSION,
                                               name_case='gen')[0]
                print('Сообщение от', colored(peer_info['first_name'] + ' ' + peer_info['last_name'], 'red') + ':',
                      end=' ')
            print(message['text'])
        if message['attachments']:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, extended=True,
                                                v=self.api.VK_API_VERSION)
        for message in messages['items'][::-1]:
            self._print_last_message(message)
        if mark_unreads_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True,
                                         v=self.api.VK_API_VERSION)


class Group_messages_parser:
    def __init__(self, api, group_id):
        self.api = api
        self.group_id = group_id

    @staticmethod
    def _print_last_message(message):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['out']:
            print('Message', colored('(Вы):', 'green'), message['text'])
        else:
            print('Message:', message['text'])
        if 'attachments' in message:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.group_id, count=count, extended=True,
                                                v=self.api.VK_API_VERSION)
        for message in messages['items'][::-1]:
            self._print_last_message(message)
        if mark_unreads_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.group_id, mark_conversation_as_read=True,
                                         v=self.api.VK_API_VERSION)
