import os
import colorama as cr
cr.init()
from lib import client, misc
from lib.commands import ls, put, get, clear, bye, pwd, cd, mkdir
from lib.commands.command import Command
from argparse import ArgumentParser
from typing import Dict

if misc.unix():
    import readline

__client: client.Client = None

# --------------------------------------------------------------------------------------------------------------------------------------- #

CMDS: Dict[str, Command] = {
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

def __parse_cmd(cmd: str) -> None:
    args = cmd.split(' ')
    for c, o in CMDS.items():
        if c == args[0]:
            o.exec(args[1:])
            return
    if not args[0].strip():
        return
    misc.print_err('Unknown command "{}" ...'.format(args[0]))

def __init(host: str, port: int = 4800) -> None:
    global __client, CMDS
    if misc.unix():
        readline.parse_and_bind('tab: complete')
        readline.set_completer(__cmd_compl)
    else:
        misc.print_wrn('Consider using a UNIX-based OS for tab-completion ... ')
    try:
        __client = client.Client(host, port)
        for k, v in CMDS.items():
            CMDS[k] = v(__client)
    except Exception as e:
        misc.print_err(e.msg)
        os._exit(1)

def __exit() -> None:
    misc.clear()

def main_loop(host: str, port: int = None) -> None:
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