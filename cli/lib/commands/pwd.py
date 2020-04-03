from lib.commands.command import Command

class Pwd(Command):
    def exec(self, args):
        print(self.cl.pwd())