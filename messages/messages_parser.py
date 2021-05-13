from datetime import datetime
from termcolor import colored, cprint


class Messages_parser:
    def __init__(self, api, peer_id=None, profile_info=None):
        self.peer_id = peer_id
        self.api = api
        self.profile_info = profile_info

    def _get_profile_name(self, response, id):
        if id >= 2000000000:  # Chat
            chat_title = self.api.messages.getChat(chat_id=id - 2000000000)['title']
            return colored('{} ({})'.format(chat_title, id), 'blue')
        elif id >= 0:  # User
            for profile in response['profiles']:
                if profile['id'] == id:
                    return colored('{} {} ({})'.format(profile['first_name'], profile['last_name'], id), 'red')
        else:  # Group
            for group in response['groups']:
                if group['id'] == abs(id):
                    return colored('{} ({})'.format(group['name'], id), 'cyan')


class Private_messages_parser(Messages_parser):
    def _print_fwd_messages(self, message, messages, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset, '-------- ', date.strftime('%Y-%m-%d %H:%M:%S'), sep='')
        group_name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset + 'От: ' + group_name)
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset + 'Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            print(' ' * offset + colored('Пересланные сообщения:', 'blue'))
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message, offset + 2)

    def _print_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if 'reply_message' in message and message['reply_message']:
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
            cprint('Пересланные сообщения:', 'blue')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(fwd_message, messages)

    def print_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count)
        for message in messages['items'][::-1]:
            self._print_message(message, messages)
        if mark_unreads_messages:
            self.api.messages.markAsRead(start_message_id=messages['items'][0]['id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True)


class Chat_messages_parser(Messages_parser):
    def _print_fwd_messages(self, message, messages, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset, '-------- ', date.strftime('%Y-%m-%d %H:%M:%S'), sep='')
        group_name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset + 'От: ' + group_name)
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset + 'Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            print(' ' * offset + colored('Пересланные сообщения:', 'blue'))
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(fwd_message, messages, offset + 2)

    def _print_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('-------- {} - №{}'.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['id']))
        if 'reply_message' in message and message['reply_message']:
            print('Ответ на сообщение №{}'.format(colored(message['reply_message']['id'], 'cyan')))
        if message['out']:
            print('Сообщение', colored('(Вы):', 'green'), end=' ')
        else:
            print('Сообщение от', self._get_profile_name(messages, message['from_id']) + ':', end=' ')
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
            cprint('Пересланные сообщения:', 'blue')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(fwd_message, messages)

    def print_messages(self, count, mark_unreads_messages=False):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, extended=True)
        for message in messages['items'][::-1]:
            self._print_message(message, messages)
        if mark_unreads_messages and messages['conversations'][0]['is_marked_unread']:
            self.api.messages.markAsRead(start_message_id=messages['conversations'][0]['last_message_id'],
                                         peer_id=self.peer_id, mark_conversation_as_read=True)


class Group_messages_parser(Messages_parser):
    def _print_fwd_messages(self, message, messages, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset + '-------- ', date.strftime('%Y-%m-%d %H:%M:%S'))
        group_name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset, 'От: ' + group_name, sep='')
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset + 'Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            print(' ' * offset + colored('Пересланные сообщения:', 'blue'))
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message, offset + 2)

    def _print_message(self, message, messages):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if 'reply_message' in message and message['reply_message']:
            print('Ответ на сообщение №{}'.format(colored(message['reply_message']['id'], 'cyan')))
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
            cprint('Пересланные сообщения:', 'blue')
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
                    self.chat_messages_parser = Chat_messages_parser(self.api, self.peer_id, self.profile_info)
                print('Сообщение в чате', self._get_profile_name(messages, message['from_id']), 'blue')
                self.chat_messages_parser._print_message(message, messages)
            elif message['from_id'] >= 0:  # User
                if self.private_messages_parser is None:
                    self.private_messages_parser = Private_messages_parser(self.api, self.peer_id, self.profile_info)
                print('Сообщение в личном диалоге с', self._get_profile_name(messages, message['from_id']))
                self.private_messages_parser._print_message(message, messages)
            else:  # Group
                if self.group_messages_parser is None:
                    self.group_messages_parser = Group_messages_parser(self.api, self.peer_id, self.profile_info)
                print('Сообщение в группе', self._get_profile_name(messages, message['from_id']), 'blue')
                self.group_messages_parser._print_message(message, messages)


class Message_details(Messages_parser):
    def _show_attachments(self, attachments):
        print('Дополнительно:')
        for attachment in attachments:
            if attachment['type'] == 'photo':
                print('Фото:', '{}_{}_{}'.format(self.profile_info['id'], attachment['photo']['id'],
                                                 attachment['photo']['access_key']))
            else:
                cprint(attachment['type'], 'cyan')

    def _print_fwd_messages(self, message, messages, offset=2):
        date = datetime.fromtimestamp(message['date'])
        print(' ' * offset + '--------', date.strftime('%Y-%m-%d %H:%M:%S'), '-', message['id'])
        name = self._get_profile_name(messages, message['from_id'])
        print(' ' * offset + 'От: ' + name)
        if 'reply_message' in message and message['reply_message']:
            print(' '*offset + 'Ответ на сообщение №{}'.format(colored(message['reply_message']['id'], 'cyan')))
        if message['text']:
            if '\n' in message['text']:
                print()
            print(' ' * offset, end='')
            print(*message['text'].split('\n'), sep='\n' + ' ' * offset)

        if message['attachments']:
            print(' ' * offset + 'Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(colored(attachment['type'], 'cyan'), end=' ')
            print()
        if 'fwd_messages' in message and message['fwd_messages']:
            cprint(' ' * offset + 'Пересланные сообщения:', 'blue')
            for fwd_message in message['fwd_messages']:
                self._print_fwd_messages(messages, fwd_message, offset + 2)
        if 'attachments' in message and message['attachments']:
            self._show_attachments(message['attachments'])

    def print_message_details(self, message_ids):
        message_details = self.api.messages.getById(message_ids=message_ids, extended=True)
        for message in message_details['items']:
            if message['peer_id'] > 2000000000:
                date = datetime.fromtimestamp(message['date'])
                print(
                    '---------- Чат: №{} - {}'.format(message['peer_id'] - 2000000000,
                                                      date.strftime('%Y-%m-%d %H:%M:%S')))
            print('Пишет:', self._get_profile_name(message_details, message['from_id']))
            print('Диалог:', self._get_profile_name(message_details, message['peer_id']))
            if 'reply_message' in message and message['reply_message']:
                print('Ответ на сообщение №{}'.format(colored(message['reply_message']['id'], 'cyan')))
            print('Сообщение:', end='')
            if '\n' in message['text']:
                print()
                for line in message['text'].split('\n'):
                    print('|', line, sep='')
            else:
                print(message['text'], sep='')
            if 'fwd_messages' in message and message['fwd_messages']:
                cprint('Пересланные сообщения:', 'blue')
                for fwd_message in message['fwd_messages']:
                    self._print_fwd_messages(fwd_message, message_details)
            if 'attachments' in message and message['attachments']:
                self._show_attachments(message['attachments'])
