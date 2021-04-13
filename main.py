import os
import re
import vk
import argparse
from cmd import Cmd
from termcolor import cprint, colored

from profile import Profile
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


def clear():
    if os.name in ('nt', 'dos'):
        os.system("cls")
    elif os.name in ('linux', 'osx', 'posix'):
        os.system("clear")
    else:
        print("\n" * 100)


class VKLogin(Cmd):
    tokens = []
    stealth = None
    default_app_id = 6121396  # Admin

    __add_parser = argparse.ArgumentParser(prog='add', description='Добавить токен')
    __add_parser.add_argument('token', metavar='TOKEN', help='Токен')

    __delete_parser = argparse.ArgumentParser(prog='delete', description='Удалить токен')
    __delete_parser.add_argument('id', metavar='ID', type=int, help='ID токена', nargs='?')
    __delete_parser.add_argument('-i', '--all-invalid', dest='invalid', action='store_true',
                                 help='Удалить все недействительные токены')

    __auth_parser = argparse.ArgumentParser(prog='auth', description='Авторизоваться')
    __auth_parser.add_argument('id', metavar='ID', type=int, help='ID токена')

    __list_parser = argparse.ArgumentParser(prog='list', description='Список токенов')
    __list_parser.add_argument('-s', '--token-status', dest='token_status', action='store_true',
                               help='Выводить действительность токена')

    __login_parser = argparse.ArgumentParser(prog='login', description='Авторизоваться по логину и паролю')
    __login_parser.add_argument('login', metavar='LOGIN', help='Логин')
    __login_parser.add_argument('password', metavar='PASSWORD', help='Пароль')
    __login_parser.add_argument('app_id', metavar='APPID', type=int, default=default_app_id, nargs='?', help='ID приложения')

    token_regex = re.compile(r'[0-9a-fA-F]{85}')

    def preloop(self):
        Cmd.preloop(self)
        self.load_tokens()
        self.prompt = '(VK-CLI)'
        self.doc_header = 'Доступные команды (для справки по конкретной команде наберите help КОМАНДА или КОМАНДА -h)'

    def __save_token_list(self):
        with open('tokens.txt', 'w') as f:
            for token in self.tokens:
                f.write(token + '\n')

    def load_tokens(self):
        if 'tokens.txt' not in os.listdir():
            return
        raw_tokens = open('tokens.txt', 'r').read()
        self.tokens = re.findall(self.token_regex, raw_tokens)
        cprint('Список токенов загружен', 'green')

    def load_options(self, args):
        if args.stealth:
            cprint('Активирован режим stealth', 'red')
            self.stealth = args.stealth

    # Commands

    @Wrapper_cmd_line_arg_parser(parser=__add_parser)
    def do_add(self, argv):
        token = argv.token.strip()
        if re.fullmatch(self.token_regex, token) is None:
            cprint('Токен не найден', 'red')
            return
        if token in self.tokens:
            cprint('Токен уже добавлен', 'red')
            return
        self.tokens.append(argv.token)
        self.__save_token_list()
        cprint('Добавлено', 'green')
        profile = Profile()
        profile.load_token(token)
        valid = profile.auth()
        if not valid:
            cprint('Ошибка аутентификации по токену', 'red')
        return

    @Wrapper_cmd_line_arg_parser(parser=__delete_parser)
    def do_delete(self, argv):
        if argv.invalid:
            for i, token in list(enumerate(self.tokens))[::-1]:
                print(i, token[:10] + '...', end=' ')
                profile = Profile()
                profile.load_token(token)
                valid = profile.auth()
                if valid:
                    cprint('Действительный', 'green')
                else:
                    self.tokens.pop(i)
                    cprint('Не действительный, удалено', 'red')
        elif argv.id:
            self.tokens.pop(argv.id)
        else:
            self.__delete_parser.print_help()
            return
        self.__save_token_list()

    @Wrapper_cmd_line_arg_parser(parser=__list_parser)
    def do_list(self, argv):
        for i, token in enumerate(self.tokens):
            print(i, token[:10] + '...', end=' ')
            if argv.token_status:
                profile = Profile()
                profile.load_token(token)
                valid = profile.auth()
                if valid:
                    print(colored('Действительный', 'green'), end='')
                else:
                    print(colored('Не действительный', 'red'), end='')
            print()

    @Wrapper_cmd_line_arg_parser(parser=__auth_parser)
    def do_auth(self, argv):
        token_id = argv.id
        if token_id + 1 > len(self.tokens):
            cprint('Токен не найден', 'red')
            return
        token = self.tokens[token_id]
        profile = Profile()
        profile.load_token(token)
        if not profile.auth():
            cprint('Ошибка аутентификации', 'red')
            return
        profile.setup(self.stealth)  # setup settings (banner, prompt)
        try:
            profile.cmdloop()
        except KeyboardInterrupt:
            clear()

    @Wrapper_cmd_line_arg_parser(parser=__login_parser)
    def do_login(self, args):
        try:
            session = vk.AuthSession(app_id=args.app_id, user_login=args.login, user_password=args.password)
        except vk.exceptions.VkAuthError:
            cprint('Ошибка авторизации', 'red')
            return
        token = session.access_token
        self.tokens.append(token)
        self.__save_token_list()
        cprint('Токен добавлен в список', 'green')

    @staticmethod
    def do_update(_):
        """Обновить локальный репозиторий (зависит от git)"""
        os.system('git pull')
        try:
            from main import VKLogin as Updated_VKLogin
        except:
            print('Ошибка запуска обновленного экземпляра')
            return
        print('Запускаю обновленный экземпляр')
        try:
            VKLogin().cmdloop()
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')
        exit()

    @staticmethod
    def do_exit(_):
        """
        Выйти
        exit
        """
        print('Выход')
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Консольная версия VK')
    parser.add_argument('-s', '--stealth', dest='stealth', action='store_true',
                        help='Не использовать методы (в случае, если пользователь не в сети), которые могут вывести '
                             'аккаунт в online')
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        maincmd = VKLogin()
        maincmd.load_options(args)
        maincmd.cmdloop()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt, выход')
        exit()
