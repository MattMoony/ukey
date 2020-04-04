from lib import misc
from lib.commands.command import Command

class Clear(Command):
    def exec(self, args):
        misc.clear()