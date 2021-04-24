from cmd import Cmd
import vk
import vk_api
from termcolor import colored, cprint
import argparse
import os
from datetime import datetime

from conversations_parser import Parser
from longpoll.profile_events import Profile_events
from messages import Private_dialog, Chat_dialog, Group_dialog
from messages.messages_parser import Auto_messages_parser
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser
from public_methods import PublicMethodsWithAuth


def clear():
    if os.name in ('nt', 'dos'):
        os.system("cls")
    elif os.name in ('linux', 'osx', 'posix'):
        os.system("clear")
    else:
        print("\n" * 100)


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'да', 'д'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'нет', 'н'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class Profile(Cmd, PublicMethodsWithAuth):
    token = None
    parser = None

    __select_parser = argparse.ArgumentParser(prog='select', description='Выбрать диалог')
    __select_parser.add_argument('id', metavar='ID', type=int, help='ID диалога', nargs='?')
    __select_parser.add_argument('-c', '--count', metavar='count', type=int, help='Количество выводимых диалогов',
                                 default=5)

    __events_parser = argparse.ArgumentParser(prog='events', description='Получать события профиля (сообщения и т.д.)')
    __events_parser.add_argument('-t', '--typing', dest='typing', action='store_true', help='Показывать печатающих')
    __events_parser.add_argument('-o', '--online', dest='online', action='store_true',
                                 help='Показывать вход/выход в online')
    __events_parser.add_argument('-r', '--read', dest='read', action='store_true',
                                 help='Помечать сообщения как прочитанные')
    __events_parser.add_argument('-s', '--sound', dest='sound', action='store_true',
                                 help='Воспроизводить звук сообщения')

    __dialogs_parser = argparse.ArgumentParser(prog='dialogs', description='Вывести все диалоги')
    __dialogs_parser.add_argument('count', metavar='COUNT', type=int, nargs='?',
                                  help='Количество выводимых диалогов', default=5)

    __unread_parser = argparse.ArgumentParser(prog='unread', description='Вывести непрочитанные')
    __unread_parser.add_argument('count', metavar='COUNT', type=int, nargs='?',
                                 help='Количество выводимых диалогов', default=5)

    __search_parser = argparse.ArgumentParser(prog='search', description='Найти сообщение')
    __search_parser.add_argument('text', metavar='TEXT', nargs='+', help='Подстрока поиска')
    __search_parser.add_argument('-c', '--count', metavar='count', type=int,
                                 help='Количество выводимых сообщений (По умолчанию: 5)', default=5)
    __search_parser.add_argument('-e', '--extended', metavar='extended', type=str2bool,
                                 help='Выводить дополнительную информацию о сообщении? (По умолчанию: да)',
                                 default=True)

    __banner_parser = argparse.ArgumentParser(prog='banner', description='Вывод баннера профиля')
    __exit_parser = argparse.ArgumentParser(prog='exit', description='Выход из профиля')

    def load_token(self, token):
        self.token = token

    def auth(self):
        session = vk.Session(self.token)
        self.api = vk.API(session, v=5.139)
        self.alternative_api = vk_api.VkApi(token=self.token)
        self.parser = Parser(self.api)
        try:
            self.api.account.getInfo()  # test token
        except vk.exceptions.VkAPIError:
            return False
        return True

    def setup(self, stealth):
        self.doc_header = 'Доступные команды (для справки по конкретной команде наберите help КОМАНДА или КОМАНДА -h)'
        self.api.stealth = stealth
        self.profile_info = self.api.account.getProfileInfo()

        # setup prompt
        self.prompt = '({} {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'])

        self.__setup_banner()

    def __setup_banner(self):
        # setup banner
        online = self.api.users.get(user_ids=self.profile_info['id'], fields=['online'])[0]['online']

        self.intro = f"{colored(self.profile_info['first_name'], 'green')} "
        self.intro += f"{colored(self.profile_info['last_name'], 'green')}"
        if 'screen_name' in self.profile_info:
            self.intro += f" ({self.profile_info['screen_name']})"
        self.intro += f" - id{self.profile_info['id']}\n"
        self.intro += f"Дата рождения: {colored(self.profile_info['bdate'], 'red')}\n"
        self.intro += f"       Онлайн: {colored('Online', 'green') if online else colored('Offline', 'red')}\n"
        if 'phone' in self.profile_info:
            self.intro += f"      Телефон: {self.profile_info['phone']}\n"
        if 'country' in self.profile_info.keys():
            self.intro += f"       Страна: {self.profile_info['country']['title']}\n"
        self.intro += f"       Статус: {colored(self.profile_info['status'], 'cyan')}"

    def _stealth_protection(self):
        if self.api.stealth:
            online = self.api.users.get(user_ids=self.profile_info['id'], fields=['online'])[0]['online']
            if not online:
                return True
        return False

    @Wrapper_cmd_line_arg_parser(parser=__dialogs_parser)
    def do_dialogs(self, argv):
        if self._stealth_protection():
            cprint('Сработала stealth защита', 'red')
            return
        count = argv.count
        if count > 100:
            count = 100
        self.parser.print_conversations(count)

    @Wrapper_cmd_line_arg_parser(parser=__unread_parser)
    def do_unread(self, argv):
        if self._stealth_protection():
            cprint('Сработала stealth защита.', 'red')
            return
        count = argv.count
        if count > 100:
            count = 100
        self.parser.print_conversations(count, filter='unread')

    @Wrapper_cmd_line_arg_parser(parser=__select_parser)
    def do_select(self, argv):
        if argv.id:
            conversation_id = argv.id
        elif not self._stealth_protection():
            if argv.count > 100:
                print('Слишком большое значение запроса последних диалогов')
            dialogs_id = self.parser.print_conversations_short(argv.count)
            answer = input('Выберите диалог>')
            if not answer.isdigit() or len(dialogs_id) < int(answer) - 1:
                cprint('Ошибка', 'red')
                return
            conversation_id = dialogs_id[int(answer)]
            if conversation_id is None:
                cprint('Ошибка', 'red')
        else:
            cprint('Сработала stealth защита. Выберите альтернативный вариант выбора диалога', 'red')
            return

        if conversation_id < 0:  # group
            group_dialog = Group_dialog()
            group_dialog.setup(self.api, self.alternative_api, self.profile_info, conversation_id)
            group_dialog.setupUI()
            try:
                group_dialog.cmdloop()
            except KeyboardInterrupt:
                print()
        elif conversation_id < 2000000000:  # private messages
            private_dialog = Private_dialog()
            private_dialog.setup(self.api, self.alternative_api, self.profile_info, conversation_id)
            private_dialog.setupUI()
            try:
                private_dialog.cmdloop()
            except KeyboardInterrupt:
                print()
        else:  # chat messages
            chat_dialog = Chat_dialog()
            chat_dialog.setup(self.api, self.alternative_api, self.profile_info, conversation_id)
            chat_dialog.setupUI()
            try:
                chat_dialog.cmdloop()
            except KeyboardInterrupt:
                print()

    @Wrapper_cmd_line_arg_parser(parser=__events_parser)
    def do_events(self, argv):
        events = Profile_events(self.api, self.alternative_api)
        events.start(argv.typing, argv.online, argv.read, argv.sound)

    @Wrapper_cmd_line_arg_parser(parser=__search_parser)
    def do_search(self, argv):
        subtext = ' '.join(argv.text)
        founded_messages = self.api.messages.search(q=subtext, count=argv.count, extended=argv.extended)
        if argv.extended:
            messages_parser = Auto_messages_parser(self.api)
            messages_parser.print_messages(founded_messages)
        else:
            for message in founded_messages['items']:
                date = datetime.fromtimestamp(message['date'])
                print('[{}] от id{}: '.format(date.strftime('%Y-%m-%d %H:%M:%S'), message['from_id']),
                      end='\n'*('\n' in message['text']))
                print(message['text'])

    @Wrapper_cmd_line_arg_parser(parser=__banner_parser)
    def do_banner(self, _):
        self.__setup_banner()
        print(self.intro)

    @Wrapper_cmd_line_arg_parser(parser=__exit_parser)
    def do_exit(self, _):
        raise KeyboardInterrupt
