from cmd import Cmd

import vk

#from messages.dialog import Dialog
from parser import Parser


class Profile(Cmd):
    profile_info = None
    peer_info = None
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
        self.peer_info = self.api.account.getProfileInfo(v=5.126)

        # setup prompt
        self.prompt = '({} {})>'.format(self.peer_info['first_name'], self.peer_info['last_name'])
        # setup banner
        self.intro = f'''{self.peer_info['first_name']} {self.peer_info['last_name']} ({self.peer_info['screen_name']}) - {self.peer_info['bdate']}
        Телефон: {self.peer_info['phone']}, Страна: {self.peer_info['country']['title']}
        Статус: {self.peer_info['status']}'''

    def do_dialogs(self, argv):
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

