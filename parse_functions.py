

class Parser:
    def __init__(self, api):
        self.api = api

    def show_user_chat(self, data):
        peer_id = data['conversation']['peer']['id']
        user = self.api.users.get(user_ids=[peer_id], v='5.52')[0]
        print('Peer: ({})'.format(peer_id), user['first_name'], user['last_name'])
        if len(data['last_message']['attachments']):
            print('Type:', data['last_message']['attachments'][0]['type'])
        if data['last_message']['from_id'] != peer_id:
            print('Message (Вы):')
        else:
            print('Message:')
        print(data['last_message']['text'])


    def show_chat_chat(self, data):
        #print(json.dumps(data, indent=8, sort_keys=True))
        title = data['conversation']['chat_settings']['title']
        last_peer = data['last_message']['from_id']

        print('Chat:', title)
        user = self.api.users.get(user_ids=[last_peer], v='5.52')[0]
        print('Peer:', user['first_name'], user['last_name'])
        if len(data['last_message']['attachments']):
            print('Other:', end=' ')
            for other in data['last_message']['attachments']:
                print(other['type'], end=' ')
            print()
        print('Message:', data['last_message']['text'])

    def show_message(self, data):
        #print(json.dumps(data, indent=8, sort_keys=True))
        if data['conversation']['peer']['type'] == 'user':
            self.show_user_chat(data)
        elif data['conversation']['peer']['type'] == 'chat':
            self.show_chat_chat(data)
        else:
            print('Peer', data['conversation']['peer']['type'], 'is not recognized')
