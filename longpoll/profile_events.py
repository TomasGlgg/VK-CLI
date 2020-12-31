from vk_api.longpoll import VkLongPoll, VkEventType
from termcolor import colored


class Profile_events:
    users = {}
    chats = {}

    def __init__(self, api, alternative_api):
        self.api = api
        self.longpoll = VkLongPoll(alternative_api)

    def _print_cache_user(self, event, case=None):
        """
        :param case: 0 - nom username, 1 - gen username, 2 - dat username
        """
        if event.user_id not in self.users:
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='nom', v='5.52')[0]
            username_nom = user_info['first_name'] + ' ' + user_info['last_name']
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='gen', v='5.52')[0]
            username_gen = user_info['first_name'] + ' ' + user_info['last_name']
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='dat', v='5.52')[0]
            username_dat = user_info['first_name'] + ' ' + user_info['last_name']
            self.users[event.user_id] = [username_nom, username_gen, username_dat]

        if case is None:
            print(self.users[event.user_id][int(event.from_me)+1], end=' ')
        else:
            print(self.users[event.user_id][case], end=' ')

    def _print_cache_chat(self, event):
        if event.chat_id not in self.chats:
            chat_info = self.api.messages.getChat(chat_id=event.chat_id - 2000000000, v=5.126)
            chat_title = chat_info['title']
            self.chats[event.chat_id] = chat_title

        print(self.chats[event.chat_id], end=' ')

    @staticmethod
    def _print_text_message(event):
        print('Текст:', event.message)
        if len(event.attachments):
            print('Дополнительно:')
            count = len(event.attachments)//2
            for i in range(count):
                attach_num = 'attach{}'.format(i+1)
                if attach_num not in event.attachments:
                    break
                attachment_type = event.attachments[attach_num+'_type']
                attachment_id = event.attachments[attach_num]
                print(attachment_type, '-', attachment_id)

    def _print_message(self, event):
        print('----------', colored('Новое сообщение:', 'red'))

        if event.from_me:
            print(colored('Вы', 'green'), '- ', end='')
        elif event.to_me:
            print(colored('От', 'red'), '- ', end='')

        if event.from_user:
            self._print_cache_user(event)
            print('- №' + str(event.message_id))

        elif event.from_chat:
            self._print_cache_user(event)
            print('в беседе')
            self._print_cache_chat(event)
            print('- №' + str(event.message_id))

        elif event.from_group:
            print('группы', event.group_id)  # TODO

        self._print_text_message(event)

    def start(self, show_typing):
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self._print_message(event)
            elif event.type == VkEventType.MESSAGE_EDIT:
                print('-------- Сообщение изменено:')
                print('Номер сообщения: №' + str(event.message_id))
                self._print_text_message(event)
            elif event.type == VkEventType.USER_TYPING and show_typing:
                print('Печатает:', end=' ')
                self._print_cache_user(event, case=0)  # case - nom
                print()
