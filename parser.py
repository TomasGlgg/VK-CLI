

class Parser:
    api = None

    def __init__(self, api):
        self.api = api

    def _printMessage(self, message):
        print(message['text'])
        if len(message['attachments']):
            print('Дополнительно:', message['attachments'][0]['type'])

    def _printPrivateMessage(self, conversation):
        peer_id = conversation['conversation']['peer']['id']
        peer_info = self.api.users.get(user_ids=[peer_id], v='5.52')[0]
        print('---------- {} {} ({}):'.format(peer_info['first_name'], peer_info['last_name'], peer_id))
        if conversation['last_message']['from_id'] != peer_id:
            print('Сообщение (Вы):', end=' ')
        else:
            print('Сообщение:', end=' ')
        self._printMessage(conversation['last_message'])

    def _printChatMessage(self, conversation):
        title = conversation['conversation']['chat_settings']['title']
        chat_id = conversation['conversation']['peer']['id']
        last_peer = conversation['last_message']['from_id']
        print('---------- Чат: {} ({})'.format(title, chat_id))
        last_peer_info = self.api.users.get(user_ids=[last_peer], v='5.52')[0]
        print('Сообщение от: {} {} ({})'.format(last_peer_info['first_name'], last_peer_info['last_name'], last_peer))
        print('Собщение:', end=' ')
        self._printMessage(conversation['last_message'])

    def printConversations(self, count):
        conversations = self.api.messages.getConversations(count=count, v='5.52')['items']
        for conversation in conversations:
            if conversation['conversation']['peer']['type'] == 'user':
                self._printPrivateMessage(conversation)
            elif conversation['conversation']['peer']['type'] == 'chat':
                self._printChatMessage(conversation)
            else:
                print('Peer', conversation['conversation']['peer']['type'], 'is not recognized')

