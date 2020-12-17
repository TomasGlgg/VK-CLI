from cmd import Cmd

import vk

from messages.dialog import Dialog
from parser import Message, User


class Profile(Cmd):
    profile_info = None
    token = None
    api = None

    def load_token(self, token):
        self.token = token

    def auth(self):
        session = vk.Session(self.token)
        self.api = vk.API(session)

    def setup(self):
        data = self.api.account.getProfileInfo(v=5.126)
        self.user = User(data)

        # setup prompt
        self.prompt = '({} {})>'.format(self.user.firs_name, self.user.last_name)
        # setup banner
        self.intro = f'''{self.user.firs_name} {self.user.last_name} ({self.user.screen_name}) - {self.user.bdate}\nТелефон: {self.user.phone}, Страна: {self.user.country.title}\nСтатус: {self.user.status}'''

    def do_dialogs(self, argv):
        if len(argv.split()) > 1:
            print('Неверное количество аргументов')
            return

        if len(argv) == 0:
            count = 10
        else:
            count = argv.split()[0]
        if int(count) > 100:
            count = str(100)
        conversations = self.api.messages.getConversations(count=count, v='5.52')['items']
        for conversation in conversations:
            message = Message(self.api, conversation)
            message.print()

    def do_select(self, argv):
        if len(argv.split()) != 1:
            print('Неверное количество аргументов')
            return
        dialog = Dialog()
        dialog.setup(self.api, self.user, int(argv.split()[0]))
        dialog.cmdloop()
