from vk_api.longpoll import VkEventType
from datetime import datetime
from termcolor import colored

from longpoll.profile_events import Profile_events


class Chat_dialog_events(Profile_events):
    def _print_message(self, event):
        print('----------', colored('Новое сообщение:', 'red'))
        if event.from_me:
            print(colored('Вы', 'green'), '- ', end='')
        elif event.to_me:
            print(colored('От', 'red'), '- ', end='')
            self._get_cache_user(event)
        last_seen = datetime.fromtimestamp(event.timestamp)
        print(last_seen.strftime('%H:%M:%S'), end=' ')
        print('- №' + str(event.message_id))
        self._print_text_message(event)

    def start(self, show_typing, chat_id):
        if chat_id >= 2000000000:
            chat_id -= 2000000000
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_chat and event.chat_id == chat_id:
                self._print_message(event)
            elif event.type == VkEventType.MESSAGE_EDIT and event.from_chat and event.chat_id == chat_id:
                print('---------- Сообщение изменено:')
                print('Номер сообщения: №' + str(event.message_id))
                self._print_text_message(event)
            elif event.type == VkEventType.USER_TYPING_IN_CHAT and event.chat_id == chat_id:
                self._get_cache_user(event)
                print('печатает...')

