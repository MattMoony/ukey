from lib import misc
from lib.commands.command import Command
from argparse import ArgumentParser
from typing import List

class Mkdir(Command):
    def exec(self, args: List[str]) -> None:
        prsr = ArgumentParser(usage='mkdir <dirname1> [<dirname2> ...]')
        prsr.add_argument(dest='d', type=str, nargs='*', help='The name of the directory to-be-created ...')
        try:
            ar = prsr.parse_args(args)
        except SystemExit:
            return
        if not ar.d:
            misc.print_err('Usage: mkdir <dirname1> [<dirname2> ...]')
            return
        for d in ar.d:
            if not self.cl.mkdir(d):
                misc.print_err('Couldn\'t create "{}" ... '.format(d))