from datetime import datetime

class Private_messages_parser:
    def __init__(self, api, peer_id):
        self.peer_id = peer_id
        self.api = api

    def _print_message(self, message):
        date = datetime.fromtimestamp(message['date'])
        print('--------', date.strftime('%Y-%m-%d %H:%M:%S'))
        if message['from_id'] != message['peer_id']:
            print('Message (Вы):', message['text'])
        else:
            print('Message:', message['text'])
        if len(message['attachments']):
            print('Дополнительно:', end=' ')
            for attachment in message['attachments']:
                print(attachment['type'], end=' ')
            print()

    def print_last_messages(self, count):
        messages = self.api.messages.getHistory(peer_id=self.peer_id, count=count, v=5.126)['items']
        for message in messages[::-1]:
            self._print_message(message)
