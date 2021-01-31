from messages.dialog import Dialog
from termcolor import colored
from argparse import ArgumentParser
from requests.exceptions import ReadTimeout

from messages.messages_parser import Chat_messages_parser
from longpoll.chat_dialog_events import Chat_dialog_events
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Chat_dialog(Dialog):
    __events_parser = ArgumentParser(prog='events', description='Вывод сообщений в реальном времени')
    __events_parser.add_argument('-t', '--typing', dest='typing', action='store_true', help='Показывать печатающих')
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
        self.parser = Chat_messages_parser(self.api, self.chat_id, self.profile_info)
        self.chat_info = self.api.messages.getChat(chat_id=self.chat_id - 2000000000)
        self.prompt = '({} {})->({})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                              self.chat_info['title'])

        self.intro = f'''
        Название чата: {self.chat_info['title']}
        Количество учатсников: {colored(self.chat_info['members_count'], 'cyan')}
        '''

    @Wrapper_cmd_line_arg_parser(parser=__read_parser)
    def do_read(self, argv):
        self.parser.print_last_messages(argv.count, mark_unreads_messages=argv.mark)

    @Wrapper_cmd_line_arg_parser(parser=__events_parser)
    def do_events(self, argv):
        events = Chat_dialog_events(self.api, self.alternative_api)
        while True:
            try:
                events.start(self.chat_id, argv.typing, argv.read, argv.sound)
            except KeyboardInterrupt:
                print('\nKeyboardInterrupt, выход')
            except ReadTimeout:
                continue
            return
