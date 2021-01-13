from datetime import datetime
from termcolor import colored


class Messages_parser:
    def __init__(self, api, peer_id=None, profile_id=None):
        self.peer_id = peer_id
        self.api = api
        self.profile_id = profile_id

    def _get_profile_name(self, response, id):
        if id >= 2000000000:
            chat_title = self.api.messages.getChat(chat_id=id - 2000000000, v=self.api.VK_API_VERSION)['title']
            return '{} ({})'.format(chat_title, id)
        elif id >= 0:
            for profile in response['profiles']:
                if profile['id'] == id:
                    return '{} {} ({})'.format(profile['first_name'], profile['last_name'], id)
        else:
            for group in response['groups']:
                if group['id'] == abs(id):
                    return '{} ({})'.format(group['name'], id)


class Private_messages_parser(Messages_parser):
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


class Chat_messages_parser(Messages_parser):
    def _print_last_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if message['out']:
            print('Сообщение', colored('(Вы):', 'green'), end=' ')
        else:
            print('Сообщение от', colored(self._get_profile_name(messages, message['from_id']), 'red') + ':', end=' ')
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


class Group_messages_parser(Messages_parser):
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
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=self.api.VK_API_VERSION)
        for message in messages['items'][::-1]:
            self._print_last_message(message)
        if mark_unreads_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True,
                                         v=self.api.VK_API_VERSION)


class Message_details(Messages_parser):
    def _print_reply_message(self, message, messages_details, offset=1):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset, '---------- {}'.format(date.strftime('%Y-%m-%d %H:%M:%S')), sep='')
        print(' ' * offset, 'Пишет: ', colored(self._get_profile_name(messages_details, message['from_id']), 'blue'), sep='')
        print(' ' * offset, 'Сообщение:', sep='', end=' ')
        if '\n' in message['text']:
            print()
            for line in message['text'].split('\n'):
                print(' ' * offset, '|', line, sep='')
        else:
            print(message['text'], sep='')
        if 'reply_message' in message:
            if message['reply_message'] is list:
                for i, reply_message in enumerate(message['reply_message']):
                    print(' ' * offset, 'Пересланное сообщение №{}:'.format(i), sep='')
                    self._print_reply_message(reply_message, messages_details, offset + 1)
            else:
                print(' ' * offset, 'Пересланное сообщение:', sep='')
                self._print_reply_message(message['reply_message'], messages_details, offset + 1)

    def _print_fwd_messages(self, fwd_messages, messages_details):
        pass

    def print_message_details(self, message_ids):
        messages_details = self.api.messages.getById(message_ids=message_ids, extended=True, v=self.api.VK_API_VERSION)
        for message in messages_details['items']:
            if message['peer_id'] > 2000000000:
                date = datetime.fromtimestamp(message['date'])
                print(
                    '---------- Чат: №{} - {}'.format(message['peer_id'] - 2000000000,
                                                      date.strftime('%Y-%m-%d %H:%M:%S')))
            print('Пишет:', colored(self._get_profile_name(messages_details, message['from_id']), 'blue'))
            print('Диалог:', colored(self._get_profile_name(messages_details, message['peer_id']), 'blue'))
            print('Сообщение:', end='')
            if '\n' in message['text']:
                print()
                for line in message['text'].split('\n'):
                    print('|', line, sep='')
            else:
                print(message['text'], sep='')
            if 'reply_message' in message:
                print('Ответ на сообщение:', sep='')
                self._print_reply_message(message['reply_message'], messages_details)
