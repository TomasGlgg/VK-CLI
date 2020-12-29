import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


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
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='acc', v='5.52')[0]
            username_acc = user_info['first_name'] + ' ' + user_info['last_name']
            user_info = self.api.users.get(user_ids=[event.user_id], name_case='dat', v='5.52')[0]
            username_dat = user_info['first_name'] + ' ' + user_info['last_name']
            self.users[event.user_id] = [username_acc, username_dat]  # 0 - acc username, 1 - dat username

        print(self.users[event.user_id][int(event.from_me)], end='')

    def _print_message(self, event):
        print('---------- Новое сообщение:')

        if event.from_me:
            print('Вы - ', end='')
        elif event.to_me:
            print('От - ', end='')

        if event.from_user:
            self._print_cache_user(event)
            print()

        elif event.from_chat:
            self._print_cache_user(event)
            print(' в беседе', event.chat_id)
        elif event.from_group:
            print('группы', event.group_id)

        print('Текст:', event.text)

    def start(self):
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self._print_message(event)
            # TODO: more events
