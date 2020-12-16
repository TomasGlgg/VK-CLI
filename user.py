from cmd import Cmd

import vk

from parse_functions import Parser


class User(Cmd):
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

        self.intro = f''' {self.profile_info['first_name']} {self.profile_info['last_name']} - {self.profile_info['screen_name']} {self.profile_info['bdate']}
        Phone: {self.profile_info['phone']}, Country: {self.profile_info['country']['title']}
        
        Status: {self.profile_info['status']} 
        '''

    def do_dialogs(self, argv):
        if len(argv.split()) > 1:
            print('Неверное количество аргументов')
            return
        count = argv.split()[0]
        if count is None:
            count = 10
        messages = self.api.messages.getConversations(count=count, v='5.52')['items']
        for message in messages:
            self.parser.show_message(message)
            print('-' * 20)
