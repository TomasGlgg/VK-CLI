from termcolor import colored
from datetime import datetime


def _printMessage(message):
    print(message['text'])
    if len(message['attachments']):
        for attachment in message['attachments']:
            print('Дополнительно:', colored(attachment['type'], 'cyan'), end=' ')
        print()


class Parser:
    api = None

    def __init__(self, api):
        self.api = api

    def _printPrivateMessage(self, conversation):
        peer_id = conversation['conversation']['peer']['id']
        peer_info = self.api.users.get(user_ids=[peer_id], v=self.api.VK_API_VERSION)[0]
        print(f'---------- {colored(peer_info["first_name"], "blue")} {colored(peer_info["last_name"], "blue")} \
({peer_id}):')
        date = datetime.fromtimestamp(conversation['last_message']['date'])
        print(date.strftime('%Y-%m-%d %H:%M:%S'))
        if 'unread_count' in conversation['conversation']:
            print(colored('Непрочитанных сообщений: {}'.format(conversation['conversation']['unread_count']), 'red'))
        if conversation['last_message']['out']:
            print('Сообщение', colored('(Вы):', 'green'), end=' ')
        else:
            print('Сообщение', colored('(Собеседник):', 'blue'), end=' ')
        _printMessage(conversation['last_message'])

    def _printChatMessage(self, conversation):
        title = colored(conversation['conversation']['chat_settings']['title'], 'blue')
        chat_id = conversation['conversation']['peer']['id']
        last_peer = conversation['last_message']['from_id']
        print('---------- Чат: {} ({})'.format(title, chat_id))
        if last_peer >= 0:
            last_peer_info = self.api.users.get(user_ids=[last_peer], v=self.api.VK_API_VERSION)[0]
            print(
                f'Сообщение от: {colored(last_peer_info["first_name"], "blue")} \
{colored(last_peer_info["last_name"], "blue")} ({last_peer})')
        else:
            last_peer_info = self.api.groups.getById(group_ids=abs(last_peer), v=self.api.VK_API_VERSION)[0]
            print(f'Сообщение от: {colored(last_peer_info["name"], "blue")} ({last_peer})')
        date = datetime.fromtimestamp(conversation['last_message']['date'])
        print(date.strftime('%Y-%m-%d %H:%M:%S'))
        print('Собщение:', end=' ')
        _printMessage(conversation['last_message'])

    def printConversationsShort(self, count):
        dialogs_ids = []
        conversations = self.api.messages.getConversations(count=count, v=self.api.VK_API_VERSION)['items']
        for i, conversation in enumerate(conversations):
            if conversation['conversation']['peer']['type'] == 'user':
                peer_id = conversation['conversation']['peer']['id']
                dialogs_ids.append(peer_id)
                peer_info = self.api.users.get(user_ids=[peer_id], v=self.api.VK_API_VERSION)[0]
                print('№{}:{} {} ({}):'.format(i, peer_info['first_name'], peer_info['last_name'], peer_id))
            elif conversation['conversation']['peer']['type'] == 'chat':
                title = conversation['conversation']['chat_settings']['title']
                chat_id = conversation['conversation']['peer']['id']
                dialogs_ids.append(chat_id)
                print('№{}:Чат: {} ({})'. format(i, title, chat_id))
            elif conversation['conversation']['peer']['type'] == 'group':
                group_id = conversation['conversation']['peer']['id']
                group_info = self.api.groups.getById(group_id=abs(group_id), v=self.api.VK_API_VERSION)['groups'][0]
                print('№{}:Группа: {} ({})'.format(i, group_info['name'], group_id))
                dialogs_ids.append(group_id)
            else:
                dialogs_ids.append(None)
                print('Peer', conversation['conversation']['peer']['type'], 'is not recognized')
        return dialogs_ids

    def printConversations(self, count, filter='all'):
        conversations = self.api.messages.getConversations(count=count, filter=filter, v=self.api.VK_API_VERSION)['items']
        for conversation in conversations:
            if conversation['conversation']['peer']['type'] == 'user':
                self._printPrivateMessage(conversation)
            elif conversation['conversation']['peer']['type'] == 'chat':
                self._printChatMessage(conversation)
            else:
                print('--------\nPeer', conversation['conversation']['peer']['type'], 'is not recognized')
