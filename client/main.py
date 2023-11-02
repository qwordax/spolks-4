import atexit
import socket
import sys

import command

def main():
    '''
    The main function of the program.
    '''
    if len(sys.argv) != 3:
        print('usage: %s <address> <port>' % sys.argv[0], file=sys.stderr)
        sys.exit(1)

    address = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    atexit.register(sock.close)

    try:
        sock.settimeout(5)
        sock.connect((address, port))

        while True:
            args = input('> ').split()

            if args == []:
                continue

            sock.settimeout(1)
            sock.send(' '.join(args).encode())

            if args[0] == 'quit':
                break

            if args[0] == 'echo':
                command.echo(sock)
            elif args[0] == 'time':
                command.time(sock)
            elif args[0] == 'upload':
                command.upload(sock, args)
            elif args[0] == 'download':
                command.download(sock, args)
            else:
                command.unknown(sock)
    except ConnectionRefusedError:
        print('error: connection refused', file=sys.stderr)
        sys.exit(1)
    except TimeoutError:
        print('error: timeout expired', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
