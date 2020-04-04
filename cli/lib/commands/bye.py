from lib.commands.command import Command

class Bye(Command):
    def exec(self, args):
        raise EOFError