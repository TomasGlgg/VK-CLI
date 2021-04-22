import os
import argparse

from wrapper_cmd_line_arg_parser import Wrapper_cmd_line_arg_parser


class PublicMethods:
    __clear_parser = argparse.ArgumentParser(prog='clear', description='Очистить консоль')

    @Wrapper_cmd_line_arg_parser(parser=__clear_parser)
    def do_clear(self, args):
        if os.name in ('nt', 'dos'):
            os.system("cls")
        elif os.name in ('linux', 'osx', 'posix'):
            os.system("clear")
        else:
            print("\n" * 100)
