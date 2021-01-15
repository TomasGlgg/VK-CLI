from vk_api.longpoll import VkEventType
from playsound import playsound

from longpoll.profile_events import Profile_events


class Private_dialog_events(Profile_events):
    def start(self, peer_id, show_typing, mark_as_read, play_sound):
        print('Получаем события... Для отмены нажмите Ctrl + c')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.peer_id == peer_id:
                self._print_message(event)
                if play_sound and event.to_me:
                    playsound('new_message.mp3')
                if mark_as_read:
                    self._mark_as_read(event.message_id, peer_id)
            elif event.type == VkEventType.MESSAGE_EDIT and event.peer_id == peer_id:
                print('---------- Сообщение изменено:')
                print('Номер сообщения: №' + str(event.message_id))
                self._print_text_from_message(event)
            elif event.type == VkEventType.USER_TYPING and show_typing and event.peer_id == peer_id:
                print('Собеседник печатает...')

