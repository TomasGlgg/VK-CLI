from cmd import Cmd
from termcolor import colored
from vk_api.utils import get_random_id


class Dialog(Cmd):
    api = None              # setup
    profile_info = None     # setup
    chat_id = None          # setup
    chat_info = None
    parser = None
    alternative_api = None  # setup

    def setup(self, api, alternative_api, profile_info, chat_id):
        self.api = api
        self.alternative_api = alternative_api
        self.profile_info = profile_info
        self.chat_id = chat_id

    def do_write(self, argv):
        """
        write [СООБЩЕНИЕ]
        """
        text = argv
        if len(text) < 1:
            print(colored('Неверное количество аргументов', 'red'))
        self.alternative_api.get_api().messages.send(peer_id=self.chat_id, random_id=get_random_id(), message=text)

    @staticmethod
    def do_exit(_):
        """
        exit
        """
        print('Выход')
        return True
