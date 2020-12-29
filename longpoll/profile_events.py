import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from termcolor import colored


class Profile_events:
    users = {}
    chats = {}

    def __init__(self, api):
        self.api = api
        token = api._session.access_token
        longpoll_api = vk_api.VkApi(token=token)
        longpoll_api._auth_token()
        self.longpoll = VkLongPoll(longpoll_api)

    def _print_cache_user(self, event):
        if event.user_id not in self.users:
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='gen', v='5.52')[0]
            username_gen = user_info['first_name'] + ' ' + user_info['last_name']
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='dat', v='5.52')[0]
            username_dat = user_info['first_name'] + ' ' + user_info['last_name']
            self.users[event.user_id] = [username_gen, username_dat]  # 0 - gen username, 1 - dat username

        print(self.users[event.user_id][int(event.from_me)], end=' ')

    def _print_cache_chat(self, event):
        if event.chat_id not in self.chats:
            chat_info = self.api.messages.getChat(chat_id=event.chat_id - 2000000000, v=5.126)
            chat_title = chat_info['title']
            self.chats[event.chat_id] = chat_title

        print(self.chats[event.chat_id], end=' ')

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

        print('Текст:', event.text)

    def start(self):
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self._print_message(event)
