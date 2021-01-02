from vk_api.longpoll import VkLongPoll, VkEventType
from termcolor import colored
from json import loads
from datetime import datetime


class Profile_events:
    users = {}
    chats = {}

    def __init__(self, api, alternative_api):
        self.api = api
        self.longpoll = VkLongPoll(alternative_api)

    def _get_cache_user(self, event, case=None):
        """
        :param case: 0 - nom username, 1 - gen username, 2 - dat username
        """
        if event.user_id not in self.users:
            if event.user_id > 0:
                user_info = self.api.users.get(user_ids=[event.user_id], name_case='nom', v=5.52)
                username_nom = user_info[0]['first_name'] + ' ' + user_info[0]['last_name']
                user_info = self.api.users.get(user_ids=[event.user_id], name_case='gen', v=5.52)[0]
                username_gen = user_info['first_name'] + ' ' + user_info['last_name']
                user_info = self.api.users.get(user_ids=[event.user_id], name_case='dat', v=5.52)[0]
                username_dat = user_info['first_name'] + ' ' + user_info['last_name']
                self.users[event.user_id] = [username_nom, username_gen, username_dat]
            else:
                group_name = self.api.groups.getById(group_ids=abs(event.user_id), v=5.52)[0]['name']
                self.users[event.user_id] = [group_name, group_name, group_name]

        if case is None:
            return self.users[event.user_id][int(event.from_me) + 1]
        else:
            return self.users[event.user_id][case]

    def _get_cache_chat(self, event):
        if event.chat_id not in self.chats:
            chat_info = self.api.messages.getChat(chat_id=event.chat_id, v=5.52)
            chat_title = chat_info['title']
            self.chats[event.chat_id] = chat_title

        return self.chats[event.chat_id]

    @staticmethod
    def _print_text_message(event):
        if event.message:
            print('Текст:', event.message)
        if len(event.attachments):
            print('Дополнительно:')
            count = len(event.attachments) // 2
            if 'reply' in event.attachments:
                reply_message = loads(event.attachments['reply'])
                print('Пересылка сообщения', colored('№{}'.format(reply_message['conversation_message_id']), 'cyan'))
            for i in range(count):
                attach_num = 'attach{}'.format(i + 1)
                if attach_num not in event.attachments:
                    break
                attachment_type = event.attachments[attach_num + '_type']
                attachment_id = event.attachments[attach_num]
                print(attachment_type, '-', attachment_id)

    def _print_message(self, event):
        print('----------', colored('Новое сообщение:', 'red'))

        if event.from_me:
            print(colored('Вы', 'green'), '- ', end='')
        elif event.to_me:
            print(colored('От', 'red'), '- ', end='')

        if event.from_user:
            print(self._get_cache_user(event))
        elif event.from_chat:
            if not event.from_me:
                print(self._get_cache_user(event), end=' ')
            print('в беседе', end=' ')
            print(self._get_cache_chat(event), end=' ')
        elif event.from_group:
            print('группы', event.group_id, end=' ')  # TODO

        last_seen = datetime.fromtimestamp(event.timestamp)
        print('-', last_seen.strftime('%H:%M:%S'), end=' ')
        print('- №' + str(event.message_id))
        self._print_text_message(event)

    def start(self, show_typing, line):
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self._print_message(event)
            elif event.type == VkEventType.MESSAGE_EDIT:
                print('----------', colored('Сообщение изменено:', 'cyan'))
                print('Номер сообщения: №' + str(event.message_id))
                self._print_text_message(event)
            elif event.type == VkEventType.USER_TYPING and show_typing:
                print('Печатает:', end=' ')
                print(self._get_cache_user(event, case=0))  # case - nom
            elif event.type == VkEventType.USER_ONLINE and line:
                print(self._get_cache_user(event, case=0), 'теперь online')
            elif event.type == VkEventType.USER_OFFLINE and line:
                print(self._get_cache_user(event, case=0), 'ушел в offline')
