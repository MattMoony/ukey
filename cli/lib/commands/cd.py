from lib import misc
from lib.commands.command import Command

class Cd(Command):
    def exec(self, args):
        if not self.cl.cd(args[0]):
            misc.print_err('Unknown directory "{}" ...'.format(args[0]))