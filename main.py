from cmd import Cmd
from os import listdir, system
from termcolor import colored
import argparse

from profile import Profile
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class VKLogin(Cmd):
    tokens = []

    __auth_parser = argparse.ArgumentParser(prog='auth', description='Авторизоваться')
    __auth_parser.add_argument('id', metavar='ID', type=int, help='ID токена')

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

    def do_list(self, _):
        """
        Список токенов
        usage: list
        """
        for i, token in enumerate(self.tokens):
            print(i, token[:10] + '...')

    @Wrapper_cmd_line_arg_parser(parser=__auth_parser)
    def do_auth(self, argv):
        token_id = argv.id
        if token_id > len(self.tokens):
            print(colored('Токен не найден', 'red'))
            return
        token = self.tokens[token_id]
        profile = Profile()
        profile.load_token(token)
        if not profile.auth():
            print(colored('Ошибка аутентификации', 'red'))
            return
        profile.setup()  # setup settings (banner, prompt)
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
        print('Запускаю обновленный экземпляр')
        try:
            VKLogin().cmdloop()
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')
        exit()

    @staticmethod
    def do_exit(_):
        '''
        Выйти
        exit
        '''
        print('Выход')
        return True


if __name__ == '__main__':
    try:
        VKLogin().cmdloop()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt, выход')
        exit()
