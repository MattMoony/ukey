from lib import misc
from lib.commands.command import Command
from argparse import ArgumentParser

class Put(Command):
    def exec(self, args):
        prsr = ArgumentParser()
        prsr.add_argument(dest='f', type=str, nargs='?')
        prsr.add_argument(dest='t', type=str, nargs='?')
        ar = prsr.parse_args(args)
        if not ar.f:
            misc.print_err('Usage: put <local-file> [<to-file>] ... ')
            return
        ulp = self.cl.ul(ar.f, ar.t)
        if not ulp:
            misc.print_err('Upload failed!')
            return
        print(' Uploaded to "%s" ... ' % ulp)