import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Profile_events:
    def __init__(self, api):
        self.api = api
        token = api._session.access_token
        longpoll_api = vk_api.VkApi(token=token)
        longpoll_api._auth_token()
        self.longpoll = VkLongPoll(longpoll_api)

    def _print_message(self, event):
        print('Новое сообщение:')

        if event.from_me:
            print('(Вы): ', end='')
        elif event.to_me:
            print('От: ', end='')

        if event.from_user:
            print(event.user_id)
        elif event.from_chat:
            print(event.user_id, 'в беседе', event.chat_id)
        elif event.from_group:
            print('группы', event.group_id)

        print('Текст: ', event.text)
        print()

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self._print_message(event)
            # TODO: more events
