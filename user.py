from cmd import Cmd
import vk


class User(Cmd):
    def load_token(self, token):
        self.token = token


    def auth(self):
        session = vk.Session(self.token)
        self.api = vk.API(session)


    def setup(self):
        self.profile_info = self.api.account.getProfileInfo(v=5.126)


        # setup prompt
        self.prompt = '({} {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'])

        # setup banner

        self.intro = f''' {self.profile_info['first_name']} {self.profile_info['last_name']} - {self.profile_info['screen_name']} {self.profile_info['bdate']}
        Phone: {self.profile_info['phone']}, Country: {self.profile_info['country']['title']}
        
        Status: {self.profile_info['status']} 
        '''





