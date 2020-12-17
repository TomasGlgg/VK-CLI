from cmd import Cmd

from parser import Conversation


class Dialog(Cmd):
    api = None
    user = None
    peer_id = None
    conversation = None

    def setup(self, api, user, peer_id):
        self.api = api
        self.user = user
        self.peer_id = peer_id
        data = self.api.messages.getConversationsById(peer_ids=[self.peer_id], v='5.52')['items'][0]
        self.conversation = Conversation(self.api, data)

        self.prompt = '({} {}) {}>'.format(self.user.firs_name, self.user.last_name, self.conversation.getName())
        self.intro = f'''Диалог {self.conversation.getName()}'''

    def do_read(self, argv):
        count = None
        if len(argv) == 1:
            count = int(argv.split()[0])
        messages = self.conversation.getMessages(count)
        for message in messages:
            message.print()
