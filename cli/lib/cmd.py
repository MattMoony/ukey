import os, readline
import colorama as cr
cr.init()
from lib import client, misc
from lib.commands import ls, put, get, clear, bye, pwd, cd, mkdir
from argparse import ArgumentParser

__client = None

# --------------------------------------------------------------------------------------------------------------------------------------- #

CMDS = {
    'ls': ls.Ls,
    'dir': ls.Ls,
    'put': put.Put,
    'get': get.Get,
    'clear': clear.Clear,
    'cls': clear.Clear,
    'bye': bye.Bye,
    'exit': bye.Bye,
    'quit': bye.Bye,
    'pwd': pwd.Pwd,
    'cd': cd.Cd,
    'mkdir': mkdir.Mkdir,
}

# --------------------------------------------------------------------------------------------------------------------------------------- #

def __cmd_compl(text, state):
    if state != 0:
        return None
    ps = readline.get_line_buffer().split()
    if len(ps) > 1:
        pass
    possb = list(filter(lambda c: c.startswith(text), CMDS.keys()))
    if len(possb) == 1:
        return possb[0]

def __parse_cmd(cmd):
    args = cmd.split(' ')
    for c, o in CMDS.items():
        if c == args[0]:
            o.exec(args[1:])
            return
    if not args[0].strip():
        return
    misc.print_err('Unknown command "{}" ...'.format(args[0]))

def __init(host, port=4800):
    global __client, CMDS
    readline.parse_and_bind('tab: complete')
    readline.set_completer(__cmd_compl)
    try:
        __client = client.Client(host, port)
        for k, v in CMDS.items():
            CMDS[k] = v(__client)
    except Exception as e:
        misc.print_err(e.msg)
        os._exit(1)

def __exit():
    misc.clear()

def main_loop(host, port=None):
    if not port:
        port = 4800
    __init(host, port)
    while True:
        try:
            print(__client.prompt())
            __parse_cmd(input('$ '))
        except KeyboardInterrupt:
            print()
        except EOFError:
            __exit()
            break

if __name__ == '__main__':
    main_loop()