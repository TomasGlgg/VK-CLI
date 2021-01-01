import io


class Wrapper_cmd_line_arg_parser:
    def __init__(self, parser):
        """Init decorator with an argparse parser to be used in parsing cmd-line options"""
        self.parser = parser
        self.help_msg = ""

    def __call__(self, f):
        def wrapped_f(*args):
            line = args[1].split()
            try:
                parsed = self.parser.parse_args(line)
            except SystemExit:
                return
            f(args[0], parsed)

        wrapped_f.__doc__ = self.__get_help(self.parser)
        return wrapped_f

    @staticmethod
    def __get_help(parser):
        """Get and return help message from 'parser.print_help()'"""
        f = io.StringIO()
        parser.print_help(file=f)
        f.seek(0)
        return f.read().rstrip()
