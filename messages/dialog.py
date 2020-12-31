from cmd import Cmd
from termcolor import colored
import vk_api
from vk_api.utils import get_random_id


class Dialog(Cmd):
    api = None
    profile_info = None
    chat_id = None
    chat_info = None
    parser = None
    messages_api = None

    def setup(self, api, profile_info, chat_id):
        self.api = api
        self.profile_info = profile_info
        self.chat_id = chat_id

    def _init_messages_api(self):
        token = self.api._session.access_token
        api = vk_api.VkApi(token=token)
        api._auth_token()
        self.messages_api = api.get_api()

    def do_write(self, argv):
        """
        write [СООБЩЕНИЕ]
        """
        text = argv
        if len(text) < 1:
            print(colored('Неверное количество аргументов', 'red'))
        if self.messages_api is None:
            self._init_messages_api()
        self.messages_api.messages.send(user_id=self.chat_id, random_id=get_random_id(), message=text)

    @staticmethod
    def do_exit(_):
        """
        exit
        """
        print('Выход')
        return True
