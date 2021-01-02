from termcolor import colored

from messages.dialog import Dialog


class Group_dialog(Dialog):
    def setupUI(self):
        self.chat_info = self.api.groups.getById(group_id=abs(self.chat_id), v=5.52)[0]

        self.intro = f'Диалог с группой {colored(self.chat_info["name"], "red")} ({self.chat_id})'

        self.prompt = '({} {})->({})>'.format(self.profile_info['first_name'], self.profile_info['last_name'],
                                              self.chat_info['name'])


