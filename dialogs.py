from cmd import Cmd

import vk
from vk.exceptions import VkAuthError, VkAPIError

from vkapi.conversation import Conversation
from vkapi.message import Message
from vkapi.user import User


class VKDialogs(Cmd):
    intro = "VK dialogs"
    prompt = ">"
    api = None
    v = None

    def __init__(self, v, token):
        """

        :param v: VK API version
        :param token: auth token
        """
        super().__init__()
        self.v = v
        self.token = token
        self.user = None
        self.dialogs = list()

    def auth(self):
        session = vk.Session(access_token=self.token)
        self.api = vk.API(session=session)

    def setup(self):
        try:
            self.auth()
            self.user = User(v=self.v, api=self.api)
            self.user.getUserInfo()
            self.prompt = f"""({self.user.getName()}) > """
            return True
        # except VkAuthError as e:
        #     print(e)
        except VkAPIError:
            print("Ошибка авторизации")
            return False

    def do_list(self, argv):
        if len(argv) == 0:
            count = '20'
        elif len(argv) > 1:
            print("Неправильное количество аргументов")
            return
        else:
            count = argv.split()[0]
        data = self.api.messages.getConversations(count=count, v=self.v)['items']
        for item in data:
            conversation = Conversation(v=self.v, api=self.api, data=item['conversation'])
            conversation.setLastMessage(item['last_message'])
            conversation.print()

    def do_back(self, argv):
        return True
