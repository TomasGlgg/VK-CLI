from cmd import Cmd

from vkapi.message import Message


class VKDialog(Cmd):
    intro = "VK dialogs"
    prompt = ">"

    conversation = None

    def __init__(self, v, api):
        super().__init__()
        self.v = v
        self.api = api

    def setup(self, conversation):
        self.conversation = conversation
        self.intro = f"""Диалог: {conversation.getName()}\n"""
        self.prompt = f"""Сообщения ({conversation.getName()}) > """

    def do_list(self, argv):
        messages = list()
        data = self.api.messages.getHistory(peer_id=self.conversation.peer.id, v=self.v)['items']
        for item in data:
            message = Message(v=self.v, api=self.api, data=item)
            messages.append(message)
            message.print()

    def do_back(self, argv):
        return True