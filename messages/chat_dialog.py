from messages.dialog import Dialog
from termcolor import colored

from messages.messages_parser import Chat_messages_parser


class Chat_dialog(Dialog):
    def setupUI(self):
        self.parser = Chat_messages_parser(self.api, self.chat_id, self.profile_info)
        self.chat_info = self.api.messages.getChat(chat_id=self.chat_id - 2000000000, v=5.126)
        self.prompt = '({} {})->({})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                              self.chat_info['title'])

        self.intro = f'''
        Название чата: {self.chat_info['title']}
        Количество учатсников: {colored(self.chat_info['members_count'], 'cyan')}
        '''

    def do_read(self, argv):
        """
        usage: read [кол-во]
        """
        if len(argv.split()) == 0:
            count = 10
        else:
            count = int(argv.split()[0])
        self.parser.print_last_messages(count)
