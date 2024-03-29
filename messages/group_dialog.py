from termcolor import colored
from argparse import ArgumentParser

from longpoll.private_dialog_events import Private_dialog_events
from messages.messages_parser import Group_messages_parser
from messages.dialog import Dialog
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Group_dialog(Dialog):
    __events_parser = ArgumentParser(prog='events', description='Вывод сообщений в реальном времени')
    __events_parser.add_argument('-r', '--read', dest='read', action='store_true',
                                 help='Помечать сообщения как прочитанные')
    __events_parser.add_argument('-s', '--sound', dest='sound', action='store_true',
                                 help='Воспроизводить звук сообщения')

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
        self.parser.print_messages(argv.count, mark_unread_messages=argv.mark)

    @Wrapper_cmd_line_arg_parser(parser=__events_parser)
    def do_events(self, argv):
        events = Private_dialog_events(self.api, self.alternative_api)
        events.start(self.chat_id, False, argv.read, argv.sound)
