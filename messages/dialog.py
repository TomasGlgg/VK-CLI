from cmd import Cmd
from termcolor import cprint
from vk_api.utils import get_random_id
import argparse

from public_methods import PublicMethodsWithAuth
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class Dialog(Cmd, PublicMethodsWithAuth):
    api = None  # setup
    profile_info = None  # setup
    chat_id = None  # setup
    chat_info = None
    parser = None
    alternative_api = None  # setup

    __delete_parser = argparse.ArgumentParser(prog='delete', description='Удалить сообщение')
    __delete_parser.add_argument('ids', metavar='IDs', type=int, nargs='+',
                                 help='ID/IDs сообщения/сообщений (разделенных через пробел)')
    __delete_parser.add_argument('-a', '--all', dest='all', action='store_true', help='Удалить у всех')

    def _stealth_protection(self):
        if self.api.stealth:
            online = self.api.users.get(user_ids=self.profile_info['id'], fields=['online'])[0]['online']
            if not online:
                return True
        return False

    def setup(self, api, alternative_api, profile_info, chat_id):
        self.api = api
        self.alternative_api = alternative_api
        self.profile_info = profile_info
        self.chat_id = chat_id
        self.doc_header = 'Доступные команды (для справки по конкретной команде наберите help КОМАНДА или КОМАНДА -h)'

    def do_write(self, argv):
        """
        write [СООБЩЕНИЕ]
        """
        if self._stealth_protection():
            cprint('Сработала stealth защита', 'red')
            return
        text = argv
        if len(text) < 1:
            cprint('Неверное количество аргументов', 'red')
        self.alternative_api.get_api().messages.send(peer_id=self.chat_id, random_id=get_random_id(), message=text)

    @Wrapper_cmd_line_arg_parser(parser=__delete_parser)
    def do_delete(self, argv):
        self.api.messages.delete(message_ids=argv.ids, delete_for_all=int(argv.all))

    @staticmethod
    def do_exit(_):
        """
        exit
        """
        print('Выход')
        return True
