from termcolor import colored
from argparse import ArgumentParser

from messages.messages_parser import Group_messages_parser
from messages.dialog import Dialog
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Group_dialog(Dialog):
    __read_parser = ArgumentParser(prog='read', description='Прочитать сообщения диалога')
    __read_parser.add_argument('count', metavar='COUNT', type=int, nargs='?',
                               help='Количество выводимых диалогов', default=10)
    __read_parser.add_argument('-m', '--mark', dest='mark', action='store_true',
                               help='Пометить сообщения как прочитанные')

    def setupUI(self):
        self.parser = Group_messages_parser(self.api, self.chat_id)
        self.chat_info = self.api.groups.getById(group_id=abs(self.chat_id), v=5.52)[0]

        self.intro = f'Диалог с группой {colored(self.chat_info["name"], "red")} ({self.chat_id})'

        self.prompt = '({} {})->({})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                              self.chat_info['name'])

    @Wrapper_cmd_line_arg_parser(parser=__read_parser)
    def do_read(self, argv):
        unread_messages_ids = self.parser.print_last_messages(argv.count, return_unread_messages_ids=argv.mark)
        if argv.mark:
            self.api.messages.markAsRead(messages_ids=unread_messages_ids, peer_id=self.chat_info['id'], v=5.52)


