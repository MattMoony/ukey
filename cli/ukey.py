from lib import misc, cmd
from argparse import ArgumentParser

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(dest='host', type=str, help='Specify the host address ... ')
    parser.add_argument('-p', '--port', dest='port', type=int, help='Specify the host port ... ')

    args = parser.parse_args()

    misc.clear()
    print(misc.center_title("""
█░░█ █░█ █▀▀ █░░█ 
█░░█ █▀▄ █▀▀ █▄▄█ 
░▀▀▀ ▀░▀ ▀▀▀ ▄▄▄█
"""))

    cmd.main_loop(args.host, args.port)

if __name__ == '__main__':
    main()