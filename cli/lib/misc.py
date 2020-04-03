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

if __name__ == '__main__':
    clear()
    print(center_title("""█░█ █▄▀ █▀▀ █▄█
█▄█ █░█ ██▄ ░█░"""))
    print_err('TEST-ERROR!')
    print_table([
        [ 'd', 'ab', 'b', ],
        [ '-', 'c', 'd', ],
    ])