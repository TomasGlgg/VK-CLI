from cmd import Cmd
import vk
import vk_api
from termcolor import colored
import argparse
import os

from conversations_parser import Parser
from longpoll.profile_events import Profile_events
from messages import Private_dialog, Chat_dialog
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Profile(Cmd):
    profile_info = None
    token = None
    api = None  # vk
    alternative_api = None  # vk_api
    parser = None

    __select_parser = argparse.ArgumentParser(prog='select', description='Выбрать диалог')
    __select_parser.add_argument('id', metavar='ID', type=int, help='ID диалога', nargs='?')
    __select_parser.add_argument('-p', '--print', metavar='count', type=int, help='Количество выводимых диалогов',
                                 default=10)

    __online_parser = argparse.ArgumentParser(prog='online', description='Получать события профиля (сообщения и т.д.)')
    __online_parser.add_argument('-t', '--typing', dest='typing', action='store_true', help='Показывать печатающих')
    __online_parser.add_argument('-l', '--line', dest='line', action='store_true',
                                 help='Показывать вход/выход в online')

    __dialogs_parser = argparse.ArgumentParser(prog='dialogs', description='Вывести все диалоги')
    __dialogs_parser.add_argument('count', metavar='COUNT', type=int, nargs='?',
                                  help='Количество выводимых диалогов', default=10)

    __unread_parser = argparse.ArgumentParser(prog='unread', description='Вывести непрочитанные')
    __unread_parser.add_argument('count', metavar='COUNT', type=int, nargs='?',
                                 help='Количество выводимых диалогов', default=10)

    def load_token(self, token):
        self.token = token

    def auth(self):
        session = vk.Session(self.token)
        self.api = vk.API(session)
        self.alternative_api = vk_api.VkApi(token=self.token)
        self.parser = Parser(self.api)

    def setup(self):
        self.profile_info = self.api.account.getProfileInfo(v=5.52)

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

    @Wrapper_cmd_line_arg_parser(parser=__dialogs_parser)
    def do_dialogs(self, argv):
        self.parser.printConversations(argv.count)

    @Wrapper_cmd_line_arg_parser(parser=__unread_parser)
    def do_unread(self, argv):
        self.parser.printConversations(argv.count, filter='unread')

    @Wrapper_cmd_line_arg_parser(parser=__select_parser)
    def do_select(self, argv):
        if argv.print:
            if argv.print > 100:
                print('Слишком большое значение запроса последних диалогов')
            dialogs_id = self.parser.printConversationsShort(argv.print)
            answer = input('Выберите диалог>')
            if not answer.isdigit() or len(dialogs_id) < int(answer) - 1:
                print(colored('Ошибка', 'red'))
                return
            conversation_id = dialogs_id[int(answer)]
        elif argv.id:
            conversation_id = argv.id
        else:
            print(colored('Неверное количество аргументов', 'red'))
            return

        if conversation_id < 2000000000:  # private messages
            private_dialog = Private_dialog()
            private_dialog.setup(self.api, self.alternative_api, self.profile_info, conversation_id)
            private_dialog.setupUI()
            try:
                private_dialog.cmdloop()
            except KeyboardInterrupt:
                os.system('cls || clear')
        else:  # chat messages
            chat_dialog = Chat_dialog()
            chat_dialog.setup(self.api, self.alternative_api, self.profile_info, conversation_id)
            chat_dialog.setupUI()
            try:
                chat_dialog.cmdloop()
            except KeyboardInterrupt:
                os.system('cls || clear')

    @Wrapper_cmd_line_arg_parser(parser=__online_parser)
    def do_online(self, argv):
        events = Profile_events(self.api, self.alternative_api)
        try:
            events.start(argv.typing, argv.line)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')

    @staticmethod
    def do_clear(_):
        """
        Очистить экран
        """
        os.system('cls || clear')

    @staticmethod
    def do_exit(_):
        """
        Выйти из текущей консоли
        exit
        """
        print('Выход')
        return True
