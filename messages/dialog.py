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

    def _stealth_protection(self):
        if self.api.stealth:
            online = self.api.users.get(user_ids=self.profile_info['id'], fields=['online'],
                                        v=self.api.VK_API_VERSION)[0]['online']
            if not online:
                return True
        return False

    def setup(self, api, alternative_api, profile_info, chat_id):
        self.api = api
        self.alternative_api = alternative_api
        self.profile_info = profile_info
        self.chat_id = chat_id

    def do_write(self, argv):
        """
        write [СООБЩЕНИЕ]
        """
        if self._stealth_protection():
            print(colored('Сработала stealth защита', 'red'))
            return
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
