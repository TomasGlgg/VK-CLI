from cmd import Cmd
from parser import Conversation

class master_dialog(Cmd):
    api = None
    peer_id = None
    conversation = None

    def setup_api(self, api, profile_info, peer_id):
        self.api = api
        self.profile_info = profile_info
        self.peer_id = peer_id
        data = self.api.messages.getConversationsById(peer_ids=[self.peer_id], v='5.52')['items'][0]
        self.conversation = Conversation(self.api, data)
