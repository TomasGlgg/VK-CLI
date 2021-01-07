from datetime import datetime
from termcolor import colored


def _get_profile_name(response, id):
    if id >= 0:
        for profile in response['profiles']:
            if profile['id'] == id:
                return '{} {} ({})'.format(profile['first_name'], profile['last_name'], id)
    else:
        for group in response['groups']:
            if group['id'] == abs(id):
                return '{} ({})'.format(group['name'], id)


class Private_messages_parser:
    def __init__(self, api, peer_id):
        self.peer_id = peer_id
        self.api = api

    @staticmethod
    def _print_private_message(message):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if message['out']:
            print('Сообщение', colored('(Вы):', 'green'), end='')
        else:
            print('Сообщение', colored('(Собеседник):', 'blue'), end='')
        if '\n' in message['text']:
            print()
        if message['text']:
            print(message['text'])
        else:
            print()

        if message['attachments']:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=self.api.VK_API_VERSION)
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

    @staticmethod
    def _print_last_message(message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if message['out']:
            print('Сообщение', colored('(Вы):', 'green'), end=' ')
        else:
            print('Сообщение от', colored(_get_profile_name(messages, message['from_id']), 'red') + ':', end=' ')
        if '\n' in message['text']:
            print()
        if message['text']:
            print(message['text'])
        else:
            print()

        if message['attachments']:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, extended=True,
                                                v=self.api.VK_API_VERSION)
        for message in messages['items'][::-1]:
            self._print_last_message(message, messages)
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
            print('Сообщение', colored('(Вы):', 'green'), end='')
        else:
            print('Сообщение', colored('(Собеседник):', 'blue'), end='')
        if '\n' in message['text']:
            print()
        if message['text']:
            print(message['text'])
        else:
            print()

        if 'attachments' in message:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

    def print_last_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.group_id, count=count, v=self.api.VK_API_VERSION)
        for message in messages['items'][::-1]:
            self._print_last_message(message)
        if mark_unreads_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.group_id, mark_conversation_as_read=True,
                                         v=self.api.VK_API_VERSION)


def _print_reply_message(message, messages_details, offset=1):
    date = datetime.fromtimestamp(message['date'])
    print(' '*offset, '---------- №{} - {}'.format(message['id'], date.strftime('%Y-%m-%d %H:%M:%S')), sep='')
    print(' '*offset, 'Пишет: ', colored(_get_profile_name(messages_details, message['from_id']), 'blue'), sep='')
    print(' '*offset, 'Сообщение:', sep='', end=' ')
    if '\n' in message['text']:
        print()
        for line in message['text'].split('\n'):
            print(' '*offset, '|', line, sep='')
    else:
        print(message['text'], sep='')
    if 'reply_message' in message:
        if message['reply_message'] is list:
            for i, reply_message in enumerate(message['reply_message']):
                print(' ' * offset, 'Пересланное сообщение №{}:'.format(i), sep='')
                _print_reply_message(reply_message, messages_details, offset + 1)
        else:
            print(' '*offset, 'Пересланное сообщение:', sep='')
            _print_reply_message(message['reply_message'], messages_details, offset+1)


def _print_fwd_messages(fwd_messages, messages_details):
    pass


def print_message_details(api, message_ids):
    messages_details = api.messages.getById(message_ids=message_ids, extended=True, v=api.VK_API_VERSION)
    for message in messages_details['items']:
        if message['peer_id'] > 2000000000:
            date = datetime.fromtimestamp(message['date'])
            print(
                '---------- Чат: №{} - {}'.format(message['peer_id'] - 2000000000, date.strftime('%Y-%m-%d %H:%M:%S')))
        print('Пишет:', colored(_get_profile_name(messages_details, message['from_id']), 'blue'))
        print('Диалог с:', colored(_get_profile_name(messages_details, message['peer_id']), 'blue'))
        print('Сообщение:', end='')
        if '\n' in message['text']:
            print()
            for line in message['text'].split('\n'):
                print('|', line, sep='')
        else:
            print(message['text'], sep='')
        if 'reply_message' in message:
            if message['reply_message'] is list:
                for i, reply_message in enumerate(message['reply_message']):
                    print('Пересланное сообщение №{}:'.format(i))
                    _print_reply_message(reply_message, messages_details)
            else:
                print('Пересланное сообщение:', sep='')
                _print_reply_message(message['reply_message'], messages_details)


