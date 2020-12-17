from cmd import Cmd
import vk

from parser import Message
from private_messages.private_dialog import Private_dialog


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
        dialog = Private_dialog()
        dialog.setup_api(self.api, self.profile_info, int(argv.split()[0]))
        dialog.cmdloop()

