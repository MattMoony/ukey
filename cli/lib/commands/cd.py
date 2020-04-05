from lib import misc
from lib.commands.command import Command
from typing import List

class Cd(Command):
    def exec(self, args: List[str]) -> None:
        if not self.cl.cd(args[0]):
            misc.print_err('Unknown directory "{}" ...'.format(args[0]))