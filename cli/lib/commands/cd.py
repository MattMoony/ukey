from lib import misc
from lib.commands.command import Command
from argparse import ArgumentParser
from typing import List

class Cd(Command):
    def exec(self, args: List[str]) -> None:
        prsr = ArgumentParser(usage='cd <dirname>')
        prsr.add_argument(dest='d', nargs='?', help='The new current working directory ... ')
        try:
            ar = prsr.parse_args(args)
        except SystemExit:
            return
        if not ar.d:
            misc.print_err('Usage: cd <dirname>')
            return
        if not self.cl.cd(ar.d):
            misc.print_err('Unknown directory "{}" ...'.format(args[0]))