from vk_api.longpoll import VkEventType
from termcolor import colored
from playsound import playsound
from datetime import datetime

from longpoll.profile_events import Profile_events


class Chat_dialog_events(Profile_events):
    def _print_message(self, event):
        print('----------', colored('Новое сообщение:', 'red'))
        if event.from_me:
            print(colored('Вы', 'green'), '- ', end='')
        elif event.to_me:
            print(colored('От', 'red'), '- ', end='')
            self._get_cached_user_name(event)
        date = datetime.fromtimestamp(event.timestamp)
        print(date.strftime('%H:%M:%S'), end=' ')
        print('- №' + str(event.message_id))
        self._print_text_from_message(event)

    def _start(self, chat_id, show_typing, mark_as_read, play_sound):
        if chat_id >= 2000000000:
            chat_id -= 2000000000
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_chat and event.chat_id == chat_id:
                self._print_message(event)
                if play_sound and event.to_me:
                    playsound('new_message.mp3')
                if mark_as_read:
                    self._mark_as_read(event.message_id, event.peer_id)
            elif event.type == VkEventType.MESSAGE_EDIT and event.from_chat and event.chat_id == chat_id:
                print('---------- Сообщение изменено:')
                print('Номер сообщения: №'.format(colored(event.message_id, 'cyan')))
                self._print_text_from_message(event)
            elif event.type == VkEventType.MESSAGE_FLAGS_SET and event.chat_id == chat_id:
                flag_bin = self.bin_with_padding(event.mask)
                if flag_bin[7] == '1':
                    print('----------',  colored('Сообщение удалено', 'red'), end='')
                    if flag_bin[17] == '1':
                        print(' (для всех)', end='')
                    print(':')
                    print('Номер сообщения: №{}'.format(event.message_id, 'cyan'))
            elif event.type == VkEventType.USER_TYPING_IN_CHAT and event.chat_id == chat_id:
                self._get_cached_user_name(event)
                print('печатает...')

