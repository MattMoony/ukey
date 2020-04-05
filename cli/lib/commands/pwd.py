from lib.commands.command import Command
from typing import List

class Pwd(Command):
    def exec(self, args: List[str]):
        print(self.cl.pwd())