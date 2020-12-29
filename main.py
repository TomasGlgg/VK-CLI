from cmd import Cmd
from os import listdir
from termcolor import colored

from profile import Profile


class VKLogin(Cmd):
    tokens = []

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
        usage: add <token>
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
        usage: delete <token>
        """
        if len(argv.split()) != 1:
            print(colored("Неправильное количество аргументов", 'red'))
            return
        self.tokens.remove(argv.split()[0])

    def do_list(self, _):
        """
        usage: list
        """
        for i, token in enumerate(self.tokens):
            print(i, token[:10] + '...')

    def do_auth(self, argv):
        """
        usage: auth <token index>
        """
        if len(argv.split()) != 1:
            print(colored("Неправильное количество аргументов", 'red'))
            return
        if not argv.split()[0].isdigit():
            print(colored('Неверный аргумент', 'red'))
            return
        token_id = int(argv.split()[0])
        if token_id > len(self.tokens):
            print(colored('Токен не найден', 'red'))
            return
        token = self.tokens[token_id]
        profile = Profile()
        profile.load_token(token)
        profile.auth()
        profile.setup()  # setup settings (banner, prompt)
        try:
            profile.cmdloop()
        except KeyboardInterrupt:
            print('Выход')
            exit()

    def do_exit(self, _):
        '''
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
