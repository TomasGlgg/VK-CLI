from messages.dialog import Dialog
from datetime import datetime

from messages.messages_parser import Private_messages_parser


class Private_dialog(Dialog):
    def setupUI(self):
        self.parser = Private_messages_parser(self.api, self.chat_id)
        fields = ['status', 'last_seen', 'online']
        self.chat_info = self.api.users.get(user_ids=[self.chat_id], fields=fields, v=5.126)[0]
        last_seen = datetime.fromtimestamp(self.chat_info['last_seen']['time'])

        self.prompt = '({} {})->({} {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                                 self.chat_info['first_name'], self.chat_info['last_name'])

        self.intro = f'''Диалог с: {self.chat_info['first_name']} {self.chat_info['last_name']}\n'''
        if self.chat_info['online'] == 1:
            self.intro += 'Online\n'
        else:
            self.intro += 'Последний вход: ' + last_seen.strftime('%Y-%m-%d %H:%M:%S') + '\n'
        self.intro += f'''Статус: {self.chat_info['status']}'''

    def do_read(self, argv):
        '''
        usage: read [count]
        '''
        if len(argv.split()) == 0:
            count = 10
        else:
            count = int(argv.split()[0])
        self.parser.print_last_messages(count)
