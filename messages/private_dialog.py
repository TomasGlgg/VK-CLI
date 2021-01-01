from messages.dialog import Dialog
from datetime import datetime
from termcolor import colored

from messages.messages_parser import Private_messages_parser
from longpoll.private_dialog_events import Private_dialog_events


class Private_dialog(Dialog):
    def setupUI(self):
        self.parser = Private_messages_parser(self.api, self.chat_id)
        fields = ['status', 'last_seen', 'online']
        self.chat_info = self.api.users.get(user_ids=[self.chat_id], fields=fields, v=5.52)[0]
        last_seen = datetime.fromtimestamp(self.chat_info['last_seen']['time'])

        self.prompt = '({} {})->({} {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                                 self.chat_info['first_name'], self.chat_info['last_name'])

        self.intro = f'''Диалог с: {colored(self.chat_info['first_name'], 'green')} {colored(self.chat_info['last_name']
                                                                                             ,'green')}\n'''
        if self.chat_info['online'] == 1:
            self.intro += colored('Online\n', 'green')
        else:
            self.intro += 'Последний вход: ' + colored(last_seen.strftime('%Y-%m-%d %H:%M:%S'), 'red') + '\n'
        self.intro += f'''Статус: {colored(self.chat_info['status'], 'cyan')}'''

    def do_read(self, argv):
        """
        usage: read [count]
        """
        if len(argv.split()) == 0:
            count = 10
        else:
            count = int(argv.split()[0])
        self.parser.print_last_messages(count)

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
        events = Private_dialog_events(self.api, self.alternative_api)
        try:
            events.start(show_typing, self.chat_id)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt, выход')

