from lib import misc
from lib.commands.command import Command
from argparse import ArgumentParser
from typing import List

class Put(Command):
    def exec(self, args: List[str]) -> None:
        prsr = ArgumentParser(usage='put <local-file> [<to-file>]')
        prsr.add_argument(dest='f', type=str, nargs='?', help='The local file name ... ')
        prsr.add_argument(dest='t', type=str, nargs='?', help='The target remote file name ... ')
        try:
            ar = prsr.parse_args(args)
        except SystemExit:
            return
        if not ar.f:
            misc.print_err('Usage: put <local-file> [<to-file>]')
            return
        ulp = self.cl.ul(ar.f, ar.t)
        if not ulp:
            misc.print_err('Upload failed!')
            return
        print(' Uploaded to "%s" ... ' % ulp)