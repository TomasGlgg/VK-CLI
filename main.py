from cmd import Cmd


class VKLogin(Cmd):
    token_list = []

    def do_add(self, argv):
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        self.token_list.append(argv.split()[0])
        print('Добавлено')
        return

    def do_delete(self, argv):
        if len(argv.split()) != 1:
            print("Неправильное количество аргументов")
            return
        self.token_list.remove(argv.split()[0])

    def do_list(self, argv):
        for token in self.token_list:
            print(token)


if __name__ == '__main__':
    VKLogin().cmdloop()
