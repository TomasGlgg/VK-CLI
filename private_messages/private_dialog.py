from private_messages.master_dialog import master_dialog


class Private_dialog(master_dialog):
    def setup_ui(self):
        self.prompt = '({} {})/({})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                             self.conversation.getName())
        self.intro = f'''
        Диалог {self.conversation.getName()}
        
        '''
