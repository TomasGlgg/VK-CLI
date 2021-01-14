from datetime import datetime
from termcolor import colored
from argparse import ArgumentParser

from messages.messages_parser import Private_messages_parser
from messages.dialog import Dialog
from longpoll.private_dialog_events import Private_dialog_events
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Private_dialog(Dialog):
    __online_parser = ArgumentParser(prog='online', description='Вывод сообщений в реальном времени')
    __online_parser.add_argument('-t', '--typing', dest='typing', action='store_true', help='Показывать печатающих')
    __online_parser.add_argument('-r', '--read', dest='read', action='store_true',
                                 help='Помечать сообщения как прочитанные')

    __read_parser = ArgumentParser(prog='read', description='Прочитать сообщения диалога')
    __read_parser.add_argument('count', metavar='COUNT', type=int, nargs='?',
                               help='Количество выводимых диалогов', default=10)
    __read_parser.add_argument('-m', '--mark', dest='mark', action='store_true',
                               help='Пометить сообщения как прочитанные')

    def __set_prompt(self):
        if self.chat_info['online']:
            online_str = colored('Online', 'green')
        else:
            online_str = colored('Offline', 'red')
        self.prompt = '({} {})->({} {} - {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                                      self.chat_info['first_name'], self.chat_info['last_name'],
                                                      online_str)

    def setupUI(self):
        self.parser = Private_messages_parser(self.api, self.chat_id)
        fields = ['status', 'last_seen', 'online']
        self.chat_info = self.api.users.get(user_ids=[self.chat_id], fields=fields, v=self.api.VK_API_VERSION)[0]
        if 'last_seen' in self.chat_info:
            last_seen = datetime.fromtimestamp(self.chat_info['last_seen']['time'])
        else:
            last_seen = None

        self.intro = f'''Диалог с: {colored(self.chat_info['first_name'], 'green')} {colored(self.chat_info['last_name']
                                                                                             , 'green')}\n'''
        if self.chat_info['online'] == 1:
            self.intro += colored('Online\n', 'green')
        elif last_seen is not None:
            self.intro += 'Последний вход: ' + colored(last_seen.strftime('%Y-%m-%d %H:%M:%S'), 'red') + '\n'
        if 'status' in self.chat_info:
            self.intro += f'''Статус: {colored(self.chat_info['status'], 'cyan')}'''
        self.__set_prompt()

    def precmd(self, line: str) -> str:
        self.chat_info['online'] = self.api.users.get(user_ids=[self.chat_id], fields='online',
                                                      v=self.api.VK_API_VERSION)[0]['online']
        self.__set_prompt()
        return line

    @Wrapper_cmd_line_arg_parser(parser=__read_parser)
    def do_read(self, argv):
        self.parser.print_last_messages(argv.count, mark_unreads_messages=argv.mark)

    @Wrapper_cmd_line_arg_parser(parser=__online_parser)
    def do_online(self, argv):
        events = Private_dialog_events(self.api, self.alternative_api)
        try:
            events.start(self.chat_id, argv.typing, argv.read)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')
