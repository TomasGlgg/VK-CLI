from vk_api.longpoll import VkEventType
from playsound import playsound
from termcolor import colored

from longpoll.profile_events import Profile_events


def bin_with_padding(num):
    num_bin = bin(num)[2:]
    num_bin = '0'*(19-len(num_bin)) + num_bin
    return num_bin[::-1]


class Private_dialog_events(Profile_events):
    def _start(self, peer_id, show_typing, mark_as_read, play_sound):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.peer_id == peer_id:
                self._print_message(event)
                if play_sound and event.to_me:
                    playsound('new_message.mp3')
                if mark_as_read:
                    self._mark_as_read(event.message_id, peer_id)
            elif event.type == VkEventType.MESSAGE_EDIT and event.peer_id == peer_id:
                print('----------', colored('Сообщение изменено:', 'red'))
                print('Номер сообщения: №' + str(event.message_id))
                self._print_text_from_message(event)
            elif event.type == VkEventType.MESSAGE_FLAGS_SET and event.peer_id == peer_id:
                flag_bin = bin_with_padding(event.mask)
                if flag_bin[7] == '1':
                    print('----------',  colored('Сообщение удалено', 'red'), end='')
                    if flag_bin[17] == '1':
                        print(' (для всех)', end='')
                    print(':')
                    print('Номер сообщения: №{}'.format(event.message_id, 'cyan'))
            elif event.type == VkEventType.USER_TYPING and show_typing and event.peer_id == peer_id:
                print('Собеседник печатает...')

