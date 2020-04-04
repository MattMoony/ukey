from lib import misc
from lib.commands.command import Command
from argparse import ArgumentParser

class Mkdir(Command):
    def exec(self, args):
        prsr = ArgumentParser()
        prsr.add_argument(dest='d', type=str, nargs='*')
        ar = prsr.parse_args(args)
        if not ar.d:
            misc.print_err('Usage: mkdir <dirname1> [<dirname2> ...]')
            return
        for d in ar.d:
            if not self.cl.mkdir(d):
                misc.print_err('Couldn\'t create "{}" ... '.format(d))