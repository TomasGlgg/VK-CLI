from cmd import Cmd
from os import listdir, system
from termcolor import colored
import argparse

from profile import Profile
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class VKLogin(Cmd):
    tokens = []
    stealth = None

    __auth_parser = argparse.ArgumentParser(prog='auth', description='Авторизоваться')
    __auth_parser.add_argument('id', metavar='ID', type=int, help='ID токена')

    __list_parser = argparse.ArgumentParser(prog='list', description='Список токенов')
    __list_parser.add_argument('-s', '--token-status', dest='token_status', action='store_true',
                               help='Выводить действительность токена')

    def preloop(self):
        Cmd.preloop(self)
        self.load_tokens()
        self.prompt = '(VK-CLI)'

    def save_token_list(self):
        with open('tokens.txt', 'w') as f:
            for token in self.tokens:
                f.write(token + '\n')

    def load_tokens(self):
        if 'tokens.txt' not in listdir():
            return
        with open('tokens.txt', 'r') as f:
            for line in f.readlines():
                self.tokens.append(line.strip())
        print(colored('Список токенов загружен', 'green'))

    def load_options(self, args):
        if args.stealth:
            print(colored('Активирован режим stealth', 'red'))
            self.stealth = args.stealth

    # Commands

    def do_add(self, argv):
        """
        Добавить токен в список
        usage: add <токен>
        """
        if len(argv.split()) != 1:
            print(colored("Неправильное количество аргументов", 'red'))
            return
        self.tokens.append(argv.split()[0])
        self.save_token_list()
        print(colored('Добавлено', 'green'))
        return

    def do_delete(self, argv):
        """
        Удалить токен из списка
        usage: delete <id>
        """
        if len(argv.split()) != 1:
            print(colored("Неправильное количество аргументов", 'red'))
            return
        self.tokens.pop(int(argv.split()[0]))
        self.save_token_list()

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
            print(colored('Токен не найден', 'red'))
            return
        token = self.tokens[token_id]
        profile = Profile()
        profile.load_token(token)
        if not profile.auth():
            print(colored('Ошибка аутентификации', 'red'))
            return
        profile.setup(self.stealth)  # setup settings (banner, prompt)
        try:
            profile.cmdloop()
        except KeyboardInterrupt:
            system('cls || clear')

    @staticmethod
    def do_update(_):
        """
        Обновить локальный репозиторий
        """
        system('git pull')
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
    try:
        vk = VKLogin()
        vk.load_options(args)
        vk.cmdloop()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt, выход')
        exit()
