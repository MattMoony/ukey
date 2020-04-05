from lib import misc
from lib.commands.command import Command
from argparse import ArgumentParser
from typing import List

class Get(Command):
    def exec(self, args: List[str]) -> None:
        prsr = ArgumentParser(usage='get <filename> [<localname>]')
        prsr.add_argument(dest='f', type=str, nargs='?', help='The target filename ... ')
        prsr.add_argument(dest='p', type=str, nargs='?', help='The local path ... ', default='')
        try:
            ar = prsr.parse_args(args)
        except SystemExit:
            return
        if not ar.f:
            misc.print_err('Usage: get <file-path>')
            return
        dlp = self.cl.dl(ar.f, ar.p)
        if not dlp:
            misc.print_err('File not found!')
            return
        print(' Downloaded to "%s" ... ' % dlp)