from datetime import datetime
from termcolor import colored


class Messages_parser:
    def __init__(self, api, peer_id=None, profile_id=None):
        self.peer_id = peer_id
        self.api = api
        self.profile_id = profile_id

    def _get_profile_name(self, response, id):
        if id >= 2000000000:  # Chat
            chat_title = self.api.messages.getChat(chat_id=id - 2000000000)['title']
            return '{} ({})'.format(chat_title, id)
        elif id >= 0:  # User
            for profile in response['profiles']:
                if profile['id'] == id:
                    return '{} {} ({})'.format(profile['first_name'], profile['last_name'], id)
        else:  # Group
            for group in response['groups']:
                if group['id'] == abs(id):
                    return '{} ({})'.format(group['name'], id)


class Private_messages_parser(Messages_parser):
    def _print_fwd_messages(self, messages, message, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset, '-------- ', date.strftime('%Y-%m-%d %H:%M:%S'), sep='')
        group_name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset, 'От: ' + group_name, sep='')
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset, 'Дополнительно:', end=' ', sep='')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            print(' '*offset, colored('Пересланные сообщения:', 'blue'), sep='')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message, offset + 2)

    def _print_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if 'reply_message' in message:
            print('Ответ на сообщение №{}'.format(colored(message['reply_message']['id'], 'cyan')))
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

        if 'fwd_messages' in message and message['fwd_messages']:
            print(colored('Пересланные сообщения:', 'blue'), sep='')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message)

    def print_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count)
        for message in messages['items'][::-1]:
            self._print_message(message, messages)
        if mark_unreads_messages:
            self.api.messages.markAsRead(start_message_id=messages['items'][0]['id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True)


class Chat_messages_parser(Messages_parser):
    def _print_fwd_messages(self, messages, message, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset, '-------- ', date.strftime('%Y-%m-%d %H:%M:%S'), sep='')
        group_name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset, 'От: ' + group_name, sep='')
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset, 'Дополнительно:', end=' ', sep='')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            print(' ' * offset, colored('Пересланные сообщения:', 'blue'), sep='')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message, offset + 2)

    def _print_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if 'reply_message' in message:
            print('Ответ на сообщение №{}'.format(colored(message['reply_message']['id'], 'cyan')))
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

        if 'fwd_messages' in message and message['fwd_messages']:
            print(colored('Пересланные сообщения:', 'blue'), sep='')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message)

    def print_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, extended=True)
        for message in messages['items'][::-1]:
            self._print_message(message, messages)
        if mark_unreads_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True)


class Group_messages_parser(Messages_parser):
    def _print_fwd_messages(self, messages, message, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset, '-------- ', date.strftime('%Y-%m-%d %H:%M:%S'), sep='')
        group_name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset, 'От: ' + group_name, sep='')
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset, 'Дополнительно:', end=' ', sep='')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            print(' ' * offset, colored('Пересланные сообщения:', 'blue'), sep='')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message, offset + 2)

    def _print_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['text']:
            if message['out']:
                print('Сообщение', colored('(Вы):', 'green'), end='')
            else:
                print('Сообщение', colored('(Собеседник):', 'blue'), end='')
            if '\n' in message['text']:
                print()
            print(message['text'])
        else:
            print()

        if 'attachments' in message:
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()

        if 'fwd_messages' in message and message['fwd_messages']:
            print(colored('Пересланные сообщения:', 'blue'), sep='')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(fwd_message, messages)

    def print_messages(self, count, mark_unread_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count)
        for message in messages['items'][::-1]:
            self._print_message(message, messages)
        if mark_unread_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True,
                                         v=self.api.VK_API_VERSION)


class Auto_messages_parser(Messages_parser):
    chat_messages_parser = None
    private_messages_parser = None
    group_messages_parser = None

    def print_messages(self, messages):
        for message in messages['items']:
            if message['from_id'] >= 2000000000:  # Chat
                if self.chat_messages_parser is None:
                    self.chat_messages_parser = Chat_messages_parser(self.api, self.peer_id, self.profile_id)
                print('Сообщение в чате', colored(self._get_profile_name(messages, message['from_id']), 'blue'))
                self.chat_messages_parser._print_message(message, messages)
            elif message['from_id'] >= 0:  # User
                if self.private_messages_parser is None:
                    self.private_messages_parser = Private_messages_parser(self.api, self.peer_id, self.profile_id)
                print('Сообщение в личном диалоге с', colored(self._get_profile_name(messages, message['from_id']), 'blue'))
                self.private_messages_parser._print_message(message, messages)
            else:  # Group
                if self.group_messages_parser is None:
                    self.group_messages_parser = Group_messages_parser(self.api, self.peer_id, self.profile_id)
                print('Сообщение в группе', colored(self._get_profile_name(messages, message['from_id']), 'blue'))
                self.group_messages_parser._print_message(message, messages)



#class Message_details(Messages_parser):
#    def _print_reply_message(self, message, message_details, offset=1):
#        date = datetime.fromtimestamp(message['date'])
#        print(' ' * offset, '---------- {}'.format(date.strftime('%Y-%m-%d %H:%M:%S')), sep='')
#        print(' ' * offset, 'Пишет: ', colored(self._get_profile_name(message_details, message['from_id']), 'blue'),
#              sep='')
#        print(' ' * offset, 'Сообщение:', sep='', end=' ')
#        if '\n' in message['text']:
#            print()
#            for line in message['text'].split('\n'):
#                print(' ' * offset, '|', line, sep='')
#        else:
#            print(message['text'], sep='')
#        if 'reply_message' in message:
#            if message['reply_message'] is list:
#                for i, reply_message in enumerate(message['reply_message']):
#                    print(' ' * offset, 'Пересланное сообщение №{}:'.format(i), sep='')
#                    self._print_reply_message(reply_message, message_details, offset + 1)
#            else:
#                print(' ' * offset, 'Пересланное сообщение:', sep='')
#                self._print_reply_message(message['reply_message'], message_details, offset + 1)
#
#    def _print_inside_fwd_message(self, message, message_details, offset):
#        if message['attachments']:
#            print(offset*' ', 'Дополнительно:', end=' ', sep='')
#            for attachment in message['attachments']:
#                print(colored(attachment['type'], 'cyan'), end=' ')
#           print()
#
#    def _print_fwd_messages(self, fwd_messages, message_details, offset=0):
#        for message in fwd_messages:
#            if 'text' in message:
#                self._print_inside_fwd_message(message, message_details, offset)
#
#    def print_message_details(self, message_ids):
#        message_details = self.api.messages.getById(message_ids=message_ids, extended=True)
#        for message in message_details['items']:
#            if message['peer_id'] > 2000000000:
#                date = datetime.fromtimestamp(message['date'])
#                print(
#                    '---------- Чат: №{} - {}'.format(message['peer_id'] - 2000000000,
#                                                      date.strftime('%Y-%m-%d %H:%M:%S')))
#            print('Пишет:', colored(self._get_profile_name(message_details, message['from_id']), 'blue'))
#            print('Диалог:', colored(self._get_profile_name(message_details, message['peer_id']), 'blue'))
#            print('Сообщение:', end='')
#            if '\n' in message['text']:
#                print()
#                for line in message['text'].split('\n'):
#                    print('|', line, sep='')
#            else:
#                print(message['text'], sep='')
#            if 'reply_message' in message:
#                print('Ответ на сообщение:', sep='')
#                self._print_reply_message(message['reply_message'], message_details)
#            if 'fwd_messages' in message and message['fwd_messages']:
#                print('Пересланные сообщения:')
#                self._print_fwd_messages(message['fwd_messages'], message_details)
