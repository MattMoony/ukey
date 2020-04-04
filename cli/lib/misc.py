import shutil, sys, os
import colorama as cr
cr.init()

def center_title(title):
    w = shutil.get_terminal_size().columns
    p = (w-max(map(lambda l: len(l), title.split('\n'))))//2
    return '\n'.join([' '*p + l for l in title.split('\n')])

def clear():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def print_err(msg, nospace=False): 
    print('%s%s%s%s' % ('' if nospace else ' ', cr.Fore.LIGHTRED_EX, msg, cr.Fore.RESET))

def print_table(tab):
    w = shutil.get_terminal_size().columns
    if type(tab) != list or type(tab[0]) != list:
        return
    ms = [max(c)+1 for c in zip(*[[len(x) for x in r] for r in tab])]
    for r in tab:
        print(' '+' '.join([('{:>'+str(ms[i])+'s}').format(c) for i, c in enumerate(r)]))

class ProgressBar(object):
    def __init__(self, _max, title='', _val=None):
        self.max = _max
        self.title = title
        self.val = _val or 0
        self.w = 20
        self.done = False
        self.__refresh()

    def update(self, val):
        if self.done:
            return
        self.val = val
        self.__refresh()
        if self.val >= self.max:
            self.end()

    def inc(self, by):
        self.update(self.val+by)

    def end(self):
        self.done = True
        print('\r {} ['.format(self.title)+'='*self.w+'] 100.00% ... ')

    def ensure_end(self):
        if not self.done:
            self.end()

    def __refresh(self):
        pc = int((self.val/self.max)*100)
        print('\r {} ['.format(self.title)+'='*(pc//(100//self.w))+'-'*(self.w-pc//(100//self.w))+'] {:6.2f}% ...'.format(pc), end='')

class FileUploadProgress(ProgressBar):
    def __init__(self, fname, title='', chunks=128):
        super().__init__(os.path.getsize(fname), title)
        self.fname = fname
        self.file = open(fname, 'rb')
        self.size = os.path.getsize(fname)
        self.len = self.size
        self.chunks = chunks

    def read(self):
        data = self.file.read(self.chunks)
        if not data:
            self.ensure_end()
            self.file.close()
        self.inc(len(data))
        return data

    def __len__(self):
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