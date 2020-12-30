from cmd import Cmd


class Dialog(Cmd):
    api = None
    profile_info = None
    chat_id = None
    chat_info = None
    parser = None

    def setup(self, api, profile_info, chat_id):
        self.api = api
        self.profile_info = profile_info
        self.chat_id = chat_id

    @staticmethod
    def do_exit(_):
        """
        exit
        """
        print('Выход')
        return True
