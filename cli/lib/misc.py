import shutil, sys, os
import colorama as cr
cr.init()
from typing import List

def center_title(title: str) -> None:
    w = shutil.get_terminal_size().columns
    p = (w-max(map(lambda l: len(l), title.split('\n'))))//2
    return '\n'.join([' '*p + l for l in title.split('\n')])

def clear() -> None:
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def unix() -> bool:
    return sys.platform != 'win32'

def print_err(msg: str, nospace: bool = False) -> None: 
    print('%s%s%s%s' % ('' if nospace else ' ', cr.Fore.LIGHTRED_EX, msg, cr.Fore.RESET))

def print_wrn(msg: str, nospace: bool = False) -> None:
    print('%s%s%s%s' % ('' if nospace else ' ', cr.Fore.LIGHTYELLOW_EX, msg, cr.Fore.RESET))

def print_table(tab: List[List[str]]) -> None:
    w = shutil.get_terminal_size().columns
    ms = [max(c)+1 for c in zip(*[[len(x) for x in r] for r in tab])]
    for r in tab:
        print(' '+' '.join([('{:>'+str(ms[i])+'s}').format(c) for i, c in enumerate(r)]))

class ProgressBar(object):
    def __init__(self, _max: int, title: str = '', _val: float = 0.) -> None:
        self.max: int   = _max
        self.title: str = title
        self.val: float = _val
        self.w: int     = 20
        self.done: bool = False
        self.__refresh()

    def update(self, val: float) -> None:
        if self.done:
            return
        self.val = val
        self.__refresh()
        if self.val >= self.max:
            self.end()

    def inc(self, by: float) -> None:
        self.update(self.val+by)

    def end(self) -> None:
        self.done = True
        print('\r {} ['.format(self.title)+'='*self.w+'] 100.00% ... ')

    def ensure_end(self) -> None:
        if not self.done:
            self.end()

    def __refresh(self) -> None:
        pc = int((self.val/self.max)*100)
        print('\r {} ['.format(self.title)+'='*(pc//(100//self.w))+'-'*(self.w-pc//(100//self.w))+'] {:6.2f}% ...'.format(pc), end='')

class FileUploadProgress(ProgressBar):
    def __init__(self, fname: str, title: str = '', chunks: int = 128) -> None:
        super().__init__(os.path.getsize(fname), title)
        self.fname: str     = fname
        self.file: file     = open(fname, 'rb')
        self.size: int      = os.path.getsize(fname)
        self.len: int       = self.size
        self.chunks: int    = chunks

    def read(self) -> bytes:
        data = self.file.read(self.chunks)
        if not data:
            self.ensure_end()
            self.file.close()
        self.inc(len(data))
        return data

    def __len__(self) -> int:
        return self.size

if __name__ == '__main__':
    clear()
    print(center_title("""█░█ █▄▀ █▀▀ █▄█
█▄█ █░█ ██▄ ░█░"""))
    print_err('TEST-ERROR!')
    print_table([
        [ 'd', 'ab', 'b', ],
        [ '-', 'c', 'd', ],
    ])

    import time
    pb = ProgressBar(100, 'Testing')
    for i in range(1,101):
        pb.update(i)
        time.sleep(0.01)