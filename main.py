from cmd import Cmd
from os import listdir

from dialogs import VKDialogs
from profile import Profile


class VKLogin(Cmd):
    intro = "VK login"
    prompt = ">"

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
        else:
            token = argv.split()[0]

        self.tokens.append(token)
        self.save_token_list()
        print('Добавлено')

    def do_delete(self, argv):
        """
        usage: delete <token>
        """
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        else:
            token = argv.split()[0]

        self.tokens.remove(token)

    def complete_delete(self, text, line, beginx, endidx):
        completions = list()
        if not text:
            completions = [token for token in self.tokens]
        for token in self.tokens:
            if token.startswith(text):
                completions.append(token)
        return completions

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
        else:
            token_pos = int(argv.split()[0])

        if token_pos > len(self.tokens):
            print('Токен не найден')
            return
        else:
            token = self.tokens[token_pos]
        dialogs = VKDialogs(v="5.128", token=token)
        if dialogs.setup():
            dialogs.cmdloop()

    def complete_auth(self, text, line, beginx, endidx):
        completions = list()
        if not text:
            completions = [str(i) for i in range(len(self.tokens))]
        for i in range(len(self.tokens)):
            if str(i).startswith(text):
                completions.append(str(i))
        return completions


if __name__ == '__main__':
    VKLogin().cmdloop()
