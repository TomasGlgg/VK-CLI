from messages.dialog import Dialog
from datetime import datetime


class Private_dialog(Dialog):
    def setupUI(self):
        fields = ['status', 'last_seen', 'online']
        self.chat_info = self.api.users.get(user_ids=[self.chat_id], fields=fields, v=5.126)[0]
        last_seen = datetime.fromtimestamp(self.chat_info['last_seen']['time'])

        self.prompt = '({} {})->({} {})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                                 self.chat_info['first_name'], self.chat_info['last_name'])

        self.intro = f'''Диалог с: {self.chat_info['first_name']} {self.chat_info['last_name']}\n'''
        if self.chat_info['online'] == 1:
            self.intro += 'Online\n'
        else:
            self.intro += 'Последний вход: ' + last_seen.strftime('%Y-%m-%d %H:%M:%S') + '\n'
        self.intro += f'''Статус: {self.chat_info['status']}'''
