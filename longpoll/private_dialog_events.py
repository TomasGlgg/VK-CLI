from vk_api.longpoll import VkEventType
from playsound import playsound

from longpoll.profile_events import Profile_events


class Private_dialog_events(Profile_events):
    def _save_event(self, event, filename, profile_id):
        if event.to_me:
            online = self.api.users.get(user_ids=[event.peer_id], fields=['online'],
                                        v=self.api.VK_API_VERSION)[0]['online']
        else:
            online = self.api.users.get(user_ids=[profile_id], fields=['online'],
                                        v=self.api.VK_API_VERSION)[0]['online']
        dump_string = '{} {} {} {} {}\n'.format(event.timestamp, int(event.from_me), online, len(event.text),
                                                event.text)
        file = open(filename, 'a')  # append dump string
        file.write(dump_string)
        file.close()

    def _start(self, peer_id, profile_id, show_typing, mark_as_read, play_sound, dump):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.peer_id == peer_id:
                self._print_message(event)
                if play_sound and event.to_me:
                    playsound('new_message.mp3')
                if mark_as_read:
                    self._mark_as_read(event.message_id, peer_id)
                if dump and event.text:
                    self._save_event(event, dump, profile_id)
            elif event.type == VkEventType.MESSAGE_EDIT and event.peer_id == peer_id:
                print('---------- Сообщение изменено:')
                print('Номер сообщения: №' + str(event.message_id))
                self._print_text_from_message(event)
            elif event.type == VkEventType.USER_TYPING and show_typing and event.peer_id == peer_id:
                print('Собеседник печатает...')

