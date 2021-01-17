from termcolor import colored
from datetime import datetime


class Parser:
    api = None

    def __init__(self, api):
        self.api = api

    @staticmethod
    def _find_profile(conversations, peer_id, key='profiles'):
        for profile in conversations[key]:
            if profile['id'] == abs(peer_id):
                return profile
        raise LookupError('Неизвестная ошибка')

    @staticmethod
    def _print_message(message):
        if message['text']:
            print(message['text'])
        if len(message['attachments']):
            for attachment in message['attachments']:
                print('Дополнительно:', colored(attachment['type'], 'cyan'), end=' ')
            print()

    def _print_private_message(self, conversations, conversation):
        peer_id = conversation['conversation']['peer']['id']
        peer_info = self._find_profile(conversations, peer_id)
        print('-' * 10, '{} {} ({})'.format(colored(peer_info['first_name'], 'blue'),
                                            colored(peer_info['last_name'], 'blue'), peer_id))
        date = datetime.fromtimestamp(conversation['last_message']['date'])
        print(date.strftime('%Y-%m-%d %H:%M:%S'))
        if conversation['last_message']['out'] and conversation['last_message']['text']:
            print('Сообщение', colored('(Вы)' + ':', 'green'), end=' ')
        else:
            print('Сообщение', colored('(Собеседник)', 'blue') + ':', end=' ')
        self._print_message(conversation['last_message'])

    def _print_chat_message(self, conversations, conversation):
        title = colored(conversation['conversation']['chat_settings']['title'], 'blue')
        chat_id = conversation['conversation']['peer']['id']
        last_peer = conversation['last_message']['from_id']
        print('---------- Чат: {} ({})'.format(title, chat_id))
        if last_peer >= 0:
            last_peer_info = self._find_profile(conversations, last_peer)
            print(
                f'Сообщение от: {colored(last_peer_info["first_name"], "blue")} \
{colored(last_peer_info["last_name"], "blue")} ({last_peer})')
        else:
            last_peer_info = self._find_profile(conversations, last_peer, key='groups')
            print(f'Сообщение от: {colored(last_peer_info["name"], "blue")} ({last_peer})')
        date = datetime.fromtimestamp(conversation['last_message']['date'])
        print(date.strftime('%Y-%m-%d %H:%M:%S'))
        if conversation['last_message']['text']:
            print('Собщение:', end=' ')
        self._print_message(conversation['last_message'])

    def _print_group_message(self, conversations, conversation):
        group_id = conversation['conversation']['peer']['local_id']
        group_info = self._find_profile(conversations, group_id, key='groups')
        print('-' * 10, '{} ({})'.format(colored(group_info['name'], 'blue'), group_id))
        date = datetime.fromtimestamp(conversation['last_message']['date'])
        print(date.strftime('%Y-%m-%d %H:%M:%S'))
        if conversation['last_message']['out'] and conversation['last_message']['text']:
            print('Сообщение', colored('(Вы)' + ':', 'green'), end=' ')
        else:
            print('Сообщение', colored('(Группа)', 'blue') + ':', end=' ')
        self._print_message(conversation['last_message'])

    def print_conversations_short(self, count):
        dialogs_ids = []
        conversations = self.api.messages.getConversations(count=count, v=self.api.VK_API_VERSION, extended=True)
        for i, conversation in enumerate(conversations['items']):
            if conversation['conversation']['peer']['type'] == 'user':
                peer_id = conversation['conversation']['peer']['id']
                peer_info = self._find_profile(conversations, peer_id)
                print('№{}:{} {} ({}):'.format(i, peer_info['first_name'], peer_info['last_name'], peer_id))
                dialogs_ids.append(peer_id)
            elif conversation['conversation']['peer']['type'] == 'chat':
                title = conversation['conversation']['chat_settings']['title']
                chat_id = conversation['conversation']['peer']['id']
                print('№{}:Чат: {} ({})'.format(i, title, chat_id))
                dialogs_ids.append(chat_id)
            elif conversation['conversation']['peer']['type'] == 'group':
                group_id = conversation['conversation']['peer']['id']
                group_info = self._find_profile(conversations, abs(group_id), key='groups')
                print('№{}:Группа: {} ({})'.format(i, group_info['name'], group_id))
                dialogs_ids.append(group_id)
            else:
                dialogs_ids.append(None)
                print('Peer', conversation['conversation']['peer']['type'], 'is not recognized')
        return dialogs_ids

    def print_conversations(self, count, filter='all'):
        conversations = self.api.messages.getConversations(count=count, filter=filter,
                                                           v=self.api.VK_API_VERSION, extended=True)
        for conversation in conversations['items']:
            if conversation['conversation']['peer']['type'] == 'user':
                self._print_private_message(conversations, conversation)
            elif conversation['conversation']['peer']['type'] == 'chat':
                self._print_chat_message(conversations, conversation)
            elif conversation['conversation']['peer']['type'] == 'group':
                self._print_group_message(conversations, conversation)
            else:
                print('--------\nPeer', conversation['conversation']['peer']['type'], 'is not recognized')
