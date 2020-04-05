from lib.commands.command import Command
from typing import List

class Bye(Command):
    def exec(self, args: List[str]) -> None:
        raise EOFError