from vk_api.longpoll import VkLongPoll, VkEventType
from termcolor import colored
from json import loads
from playsound import playsound
from requests.exceptions import ReadTimeout
from datetime import datetime


class Profile_events:
    users = {}
    chats = {}
    groups = {}

    def __init__(self, api, alternative_api):
        self.api = api
        self.longpoll = VkLongPoll(alternative_api)

    @staticmethod
    def bin_with_padding(num):
        num_bin = bin(num)[2:]
        num_bin = '0' * (19 - len(num_bin)) + num_bin
        return num_bin[::-1]

    def _get_cached_user_name(self, event, case=None):
        """
        :param case: 0 - nom username, 1 - gen username, 2 - dat username
        """
        if event.user_id not in self.users:
            if event.user_id > 0:
                user_info = self.api.users.get(user_ids=[event.user_id], name_case='nom')[0]
                username_nom = user_info['first_name'] + ' ' + user_info['last_name']
                user_info = self.api.users.get(user_ids=[event.user_id], name_case='gen')[0]
                username_gen = user_info['first_name'] + ' ' + user_info['last_name']
                user_info = self.api.users.get(user_ids=[event.user_id], name_case='dat')[0]
                username_dat = user_info['first_name'] + ' ' + user_info['last_name']
                self.users[event.user_id] = [username_nom, username_gen, username_dat]
            else:
                group_name = self.api.groups.getById(group_ids=abs(event.user_id))['groups'][0]['name']
                self.users[event.user_id] = [group_name, group_name, group_name]

        if case is None:
            return self.users[event.user_id][int(event.from_me) + 1]
        else:
            return self.users[event.user_id][case]

    def _get_cached_chat_name(self, event):
        if event.chat_id not in self.chats:
            chat_info = self.api.messages.getChat(chat_id=event.chat_id)
            chat_title = chat_info['title']
            self.chats[event.chat_id] = chat_title

        return self.chats[event.chat_id]

    def _get_cached_group_name(self, event):
        group_id = abs(event.peer_id)
        if group_id not in self.groups:
            group_info = self.api.groups.getById(group_ids=[group_id])
            group_name = group_info['groups'][0]['name']
            self.groups[group_id] = group_name

        return self.groups[group_id]

    @staticmethod
    def _print_text_from_message(event):
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
            print(colored(self._get_cached_user_name(event), 'blue'), end=' ')
        elif event.from_chat:
            if not event.from_me:
                print(colored(self._get_cached_user_name(event), 'blue'), end=' ')
            print('в беседе', end=' ')
            print(colored(self._get_cached_chat_name(event), 'blue'), end=' ')
        elif event.from_group:
            print('группы', colored(self._get_cached_group_name(event), 'blue'), end=' ')

        date = datetime.fromtimestamp(event.timestamp)
        print('-', date.strftime('%Y-%m-%d %H:%M:%S'), end=' ')
        print('- №' + str(event.message_id))
        self._print_text_from_message(event)

    def _mark_as_read(self, message_id, peer_id):
        self.api.messages.markAsRead(start_message_id=message_id, peer_id=peer_id, mark_conversation_as_read=True)

    def _start(self, show_typing, online, mark_as_read, play_sound):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self._print_message(event)
                if play_sound and event.to_me:
                    playsound('new_message.mp3')
                if mark_as_read:
                    self._mark_as_read(event.message_id, event.peer_id)
            elif event.type == VkEventType.MESSAGE_EDIT:
                print('----------', colored('Сообщение изменено:', 'cyan'))
                print('Номер сообщения: №'.format(colored(event.message_id, 'cyan')))
                self._print_text_from_message(event)
            elif event.type == VkEventType.MESSAGE_FLAGS_SET:
                flag_bin = self.bin_with_padding(event.mask)
                if flag_bin[7] == '1':
                    print('----------',  colored('Сообщение удалено', 'red'), end='')
                    if flag_bin[17] == '1':
                        print(' (для всех)', end='')
                    print(':')
                    print('Номер сообщения: №{}'.format(event.message_id, 'cyan'))
            elif event.type == VkEventType.USER_TYPING and show_typing:
                print('Печатает:', end=' ')
                print(colored(self._get_cached_user_name(event, case=0), 'blue'))  # case - nom
            elif event.type == VkEventType.USER_ONLINE and online:
                print(self._get_cached_user_name(event, case=0), 'теперь online')
            elif event.type == VkEventType.USER_OFFLINE and online:
                print(self._get_cached_user_name(event, case=0), 'ушел в offline')

    def start(self, *args):
        print('Получаем события... Для отмены нажмите Ctrl + c')
        while True:
            try:
                self._start(*args)
            except ReadTimeout:
                print('Разрыв связи, переподключение..')
            except KeyboardInterrupt:
                print('\nKeyboardInterrupt, выход')
                return
