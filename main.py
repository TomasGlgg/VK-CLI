from cmd import Cmd
from os import listdir
from user import User

class VKLogin(Cmd):
    token_list = []

    def preloop(self):
        Cmd.preloop(self)
        self.load_token_list()

    def save_token_list(self):
        file = open('tokens.txt', 'w')
        for token in self.token_list:
            file.write(token+'\n')

    def load_token_list(self):
        if 'tokens.txt' not in listdir(): return
        file = open('tokens.txt', 'r')
        for line in file.readlines():
            self.token_list.append(line.strip())
        print('Список токенов загружен')

    # Commands

    def do_add(self, argv):
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        self.token_list.append(argv.split()[0])
        self.save_token_list()
        print('Добавлено')
        return

    def do_delete(self, argv):
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        self.token_list.remove(argv.split()[0])

    def do_list(self, argv):
        for id, token in enumerate(self.token_list):
            print(id, token[:10]+'...')

    def do_auth(self, argv):
        '''
        auth <token index>
        '''
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return

        token_id = int(argv.split()[0])
        if token_id>len(self.token_list):
            print('Токен не найден')
            return
        token = self.token_list[token_id]
        user = User()
        user.load_token(token)
        user.auth()
        user.setup()  # setup settings (banner, prompt)
        user.cmdloop()


if __name__ == '__main__':
    VKLogin().cmdloop()
