from lib.commands.command import Command
from lib import misc
from argparse import ArgumentParser
import colorama as cr
cr.init()
from typing import List

class Ls(Command):
    def exec(self, args: List[str]) -> None:
        prsr = ArgumentParser(usage='ls [-lat] [<dirname>]')
        prsr.add_argument(dest='d', type=str, nargs='?', help='Target directory\'s name ... ')
        prsr.add_argument('-l', dest='l', action='store_true', help='Display as list ... ')
        prsr.add_argument('-a', dest='a', action='store_true', help='Show all files ... ')
        prsr.add_argument('-t', dest='t', action='store_true', help='Also show detected MIME-Types ... ')
        try:
            ar = prsr.parse_args(args)
        except SystemExit:
            return
        _dir = self.cl.ls(ar.d)
        if type(_dir) != list:
            misc.print_err('Unknown directory "{}" ...'.format(ar.d))
            return
        _dir = list(filter(lambda f: not f['name'].startswith('.') or ar.a, _dir))
        if ar.l:
            misc.print_table(list(map(lambda f: [ 'd' if f['type'] == 'dir' else '-', f['type'] if ar.t else '', f['name'] ], _dir)))
        else:
            print('   '.join(map(lambda f: f['name'] if f['type'] != 'dir' else '{}{}{}'.format(cr.Fore.LIGHTCYAN_EX, f['name'], cr.Fore.RESET), _dir)))