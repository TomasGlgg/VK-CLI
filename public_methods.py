import os
import argparse
import vk
import requests
from tempfile import NamedTemporaryFile
from termcolor import cprint
from playsound import playsound

from messages.messages_parser import Message_details
from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class PublicMethods:
    __clear_parser = argparse.ArgumentParser(prog='clear', description='Очистить консоль')

    @Wrapper_cmd_line_arg_parser(parser=__clear_parser)
    def do_clear(self, _):
        if os.name in ('nt', 'dos'):
            os.system("cls")
        elif os.name in ('linux', 'osx', 'posix'):
            os.system("clear")
        else:
            print("\n" * 100)


class PublicMethodsWithAuth(PublicMethods):
    api = None  # vk
    alternative_api = None  # vk_api
    profile_info = None

    __message_details_parser = argparse.ArgumentParser(prog='message_details',
                                                       description='Показать подробности сообщения')
    __message_details_parser.add_argument('ids', metavar='IDs', type=int, nargs='+',
                                          help='ID/IDs сообщения/сообщений (разделенных через пробел)')

    __play_parser = argparse.ArgumentParser(prog='play', description='Воспроизвести аудиосообщение')
    __play_parser.add_argument('ids', metavar='IDs', type=int, nargs='+',
                               help='ID/IDs сообщения/сообщений (разделенных через пробел)')

    def _stealth_protection(self):
        if self.api.stealth:
            online = self.api.messages.getLastActivity(user_id=self.profile_info['id'])['online']
            if not online:
                return True
        return False

    @Wrapper_cmd_line_arg_parser(parser=__message_details_parser)
    def do_message_details(self, argv):
        message_ids = argv.ids
        message_details = Message_details(self.api, None, self.profile_info)
        try:
            message_details.print_message_details(message_ids)
        except vk.exceptions.VkAPIError:
            cprint('Ошибка', 'red')

    @Wrapper_cmd_line_arg_parser(parser=__play_parser)
    def do_play(self, argv):
        def play_audio(link):
            tmp_file = NamedTemporaryFile(delete=False)
            mp3 = requests.get(link, stream=True)
            print('Скачивается аудиосообщение №{}'.format(message['id']))
            for chunk in mp3.iter_content(chunk_size=4 * (2 ** 10)):  # chunk_size = 4KB
                if chunk:
                    tmp_file.write(chunk)
            tmp_file.close()
            print('Воспроизведение')
            playsound(tmp_file.name)

        messages = self.api.messages.getById(message_ids=argv.ids)['items']
        for message in messages:
            if 'attachments' not in message or not message['attachments']:
                print('Сообщение №{} не содержит аудиосообщения'.format(message['id']))
                continue
            for attachment in message['attachments']:
                if attachment['type'] == 'audio_message':
                    audio_link = attachment['audio_message']['link_mp3']
                    try:
                        play_audio(audio_link)
                    except KeyboardInterrupt:
                        pass
                    break
            else:
                print('Сообщение №{} не содержит аудиосообщения'.format(message['id']))
