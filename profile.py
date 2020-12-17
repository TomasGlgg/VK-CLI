from cmd import Cmd
import vk

from conversations_parser import Parser
from messages.private_dialog import Private_dialog


class Profile(Cmd):
    profile_info = None
    token = None
    api = None
    parser = None

    def load_token(self, token):
        self.token = token

    def auth(self):
        session = vk.Session(self.token)
        self.api = vk.API(session)
        self.parser = Parser(self.api)

    def setup(self):
        self.profile_info = self.api.account.getProfileInfo(v=5.126)

        # setup prompt
        self.prompt = '({} {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'])
        # setup banner
        self.intro = f'''{self.profile_info['first_name']} {self.profile_info['last_name']} ({self.profile_info['screen_name']}) - {self.profile_info['bdate']}
        Телефон: {self.profile_info['phone']}\n'''
        if 'country' in self.profile_info.keys():
            self.intro += f'''Страна: {self.profile_info['country']['title']}\n'''
        self.intro += f'''Статус: {self.profile_info['status']}'''

    def do_dialogs(self, argv):
        '''
        usage: dialogs [count]
        '''
        if len(argv.split()) > 1:
            print('Неверное количество аргументов')
            return
        elif len(argv) == 1:
            count = int(argv.split()[0])
            if count > 100:
                count = 100
        else:
            count = 10
        self.parser.printConversations(count)

    def do_select(self, argv):
        '''
        usage: select <chat id>
        '''
        if len(argv.split()) != 1:
            print('Неверное количество аргументов')
            return
        conversation_id = int(argv.split()[0])
        conversation_info = self.api.messages.getConversationsById(peer_ids=[conversation_id], v=5.126)['items'][0]
        if conversation_info['peer']['type'] == 'user':
            private_dialog = Private_dialog()
            private_dialog.setup(self.api, self.profile_info, conversation_id)
            private_dialog.setupUI()
            private_dialog.cmdloop()
        elif conversation_info['peer']['type'] == 'chat':
            pass  # TODO: chat dialog
