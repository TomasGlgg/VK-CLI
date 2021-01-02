from messages.dialog import Dialog
from datetime import datetime
from termcolor import colored
from argparse import ArgumentParser

from messages.messages_parser import Private_messages_parser
from longpoll.private_dialog_events import Private_dialog_events
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Private_dialog(Dialog):
    __online_parser = ArgumentParser(prog='online', description='Вывод сообщений в реальном времени')
    __online_parser.add_argument('-t', '--typing', dest='typing', action='store_true', help='Показывать печатающих')

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
        self.chat_info = self.api.users.get(user_ids=[self.chat_id], fields=fields, v=5.52)[0]
        last_seen = datetime.fromtimestamp(self.chat_info['last_seen']['time'])

        self.intro = f'''Диалог с: {colored(self.chat_info['first_name'], 'green')} {colored(self.chat_info['last_name']
                                                                                             , 'green')}\n'''
        if self.chat_info['online'] == 1:
            self.intro += colored('Online\n', 'green')
        else:
            self.intro += 'Последний вход: ' + colored(last_seen.strftime('%Y-%m-%d %H:%M:%S'), 'red') + '\n'
        self.intro += f'''Статус: {colored(self.chat_info['status'], 'cyan')}'''
        self.__set_prompt()

    def precmd(self, line: str) -> str:
        self.chat_info['online'] = self.api.users.get(user_ids=[self.chat_id], fields='online', v=5.52)[0]['online']
        self.__set_prompt()
        return line

    def do_read(self, argv):
        """
        Прочитать сообщения
        usage: read [count]
        """
        if len(argv.split()) == 0:
            count = 10
        else:
            count = int(argv.split()[0])
        self.parser.print_last_messages(count)

    @Wrapper_cmd_line_arg_parser(parser=__online_parser)
    def do_online(self, argv):
        events = Private_dialog_events(self.api, self.alternative_api)
        try:
            events.start(argv.typing, self.chat_id)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')
