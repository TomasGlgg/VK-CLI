from cmd import Cmd
from os import listdir

from profile import Profile


class VKLogin(Cmd):
    tokens = []

    def preloop(self):
        Cmd.preloop(self)
        self.load_tokens()

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
        print('Список токенов загружен')

    # Commands

    def do_add(self, argv):
        """
        usage: add <token>
        """
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        self.tokens.append(argv.split()[0])
        self.save_token_list()
        print('Добавлено')
        return

    def do_delete(self, argv):
        """
        usage: delete <token>
        """
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        self.tokens.remove(argv.split()[0])

    def do_list(self, argv):
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
            print("Неправильное количество аргументов")
            return
        if not argv.split()[0].isdigit():
            print('Неверный аргумент')
            return
        token_id = int(argv.split()[0])
        if token_id > len(self.tokens):
            print('Токен не найден')
            return
        token = self.tokens[token_id]
        profile = Profile()
        profile.load_token(token)
        profile.auth()
        profile.setup()  # setup settings (banner, prompt)
        profile.cmdloop()


if __name__ == '__main__':
    VKLogin().cmdloop()
