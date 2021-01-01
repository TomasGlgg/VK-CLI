from cmd import Cmd
import vk
import vk_api
from termcolor import colored
import argparse

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

    __select_parser = argparse.ArgumentParser(prog='select')
    __select_parser.add_argument('id', metavar='ID', type=int, help='ID диалога', nargs='?')
    __select_parser.add_argument('-p', '--print', metavar='count', type=int, help='Выбрать из count последних диалогов')

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

    def do_dialogs(self, argv):
        """
        Вывести все диалоги
        usage: dialogs [кол-во]
        """
        argv = argv.split()
        if len(argv) > 1:
            print(colored('Неверное количество аргументов', 'red'))
            return
        elif len(argv) == 1:
            if argv[0].isdigit():
                count = int(argv[0])
                if count > 100:
                    count = 100
            else:
                print(colored('Неверный аргумент', 'red'))
                return
        else:
            count = 10
        self.parser.printConversations(count)

    def do_unread(self, argv):
        """
        Вывести все непрочитанные диалоги
        usage: unread [кол-во]
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
        self.parser.printConversations(count, filter='unread')

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
                print('\nВыход')
                exit()
        else:  # chat messages
            chat_dialog = Chat_dialog()
            chat_dialog.setup(self.api, self.alternative_api, self.profile_info, conversation_id)
            chat_dialog.setupUI()
            try:
                chat_dialog.cmdloop()
            except KeyboardInterrupt:
                print('\nВыход')
                exit()

    def do_online(self, argv):
        """
        Вывод сообщений в реальном времени
        usage: online [аргументы]
        -s     показывать печатающих
        """
        show_typing = False
        argv = argv.split()
        if len(argv) > 1:
            print(colored('Неверное количество аргументов', 'red'))
            return
        elif len(argv) == 1:
            if argv[0] == '-s':
                show_typing = True
            else:
                print(colored('Нераспознанный аргумент ' + argv[0], 'red'))
                return
        events = Profile_events(self.api, self.alternative_api)
        try:
            events.start(show_typing)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')

    @staticmethod
    def do_exit(_):
        """
        Выйти из текущей консоли
        exit
        """
        print('Выход')
        return True

