import os
import argparse
import vk
from termcolor import cprint

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

    @Wrapper_cmd_line_arg_parser(parser=__message_details_parser)
    def do_message_details(self, argv):
        message_ids = argv.ids
        message_details = Message_details(self.api, None, self.profile_info)
        try:
            message_details.print_message_details(message_ids)
        except vk.exceptions.VkAPIError:
            cprint('Ошибка', 'red')
