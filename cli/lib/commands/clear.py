from lib import misc
from lib.commands.command import Command
from typing import List

class Clear(Command):
    def exec(self, args: List[str]) -> None:
        misc.clear()