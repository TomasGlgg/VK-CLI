from cmd import Cmd
import vk
from termcolor import colored

from conversations_parser import Parser
from messages import Private_dialog, Chat_dialog


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
        self.intro = f"{colored(self.profile_info['first_name'], 'green')} "
        self.intro += f"{colored(self.profile_info['last_name'], 'green')} ({self.profile_info['screen_name']}) "
        self.intro += f"- id{self.profile_info['id']}\n"
        self.intro += f"Дата рождения: {colored(self.profile_info['bdate'], 'red')}\n"
        self.intro += f"      Телефон: {self.profile_info['phone']}\n"
        if 'country' in self.profile_info.keys():
            self.intro += f"       Страна: {self.profile_info['country']['title']}\n"
        self.intro += f"       Статус: {colored(self.profile_info['status'], 'cyan')}"

    def do_dialogs(self, argv):
        """
        usage: dialogs [count]
        """
        if len(argv.split()) > 1:
            print(colored('Неверное количество аргументов', 'red'))
            return
        elif len(argv) == 1:
            count = int(argv.split()[0])
            if count > 100:
                count = 100
        else:
            count = 10
        self.parser.printConversations(count)

    def do_select(self, argv):
        """
        usage: select <chat id>
        """
        if len(argv.split()) != 1:
            print(colored('Неверное количество аргументов', 'red'))
            return
        conversation_id = int(argv.split()[0])
        # conversation_info = self.api.messages.getConversationsById(peer_ids=[conversation_id], v=5.126)['items'][0]
        if conversation_id < 2000000000:  # private messages
            private_dialog = Private_dialog()
            private_dialog.setup(self.api, self.profile_info, conversation_id)
            private_dialog.setupUI()
            try:
                private_dialog.cmdloop()
            except KeyboardInterrupt:
                print('\nВыход')
                exit()
        else:  # chat messages
            chat_dialog = Chat_dialog()
            chat_dialog.setup(self.api, self.profile_info, conversation_id)
            chat_dialog.setupUI()
            try:
                chat_dialog.cmdloop()
            except KeyboardInterrupt:
                print('\nВыход')
                exit()

    def do_exit(self, _):
        '''
        exit
        '''
        print('Выход')
        return True
