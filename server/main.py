import filelock

import multiprocessing as proc
import socket
import sys

import command
import length
import timeout

N_MIN = 1
'''
The minimum number of threads.
'''

N_MAX = 3
'''
The maximum number of threads.
'''

def handle(sock):
    '''
    Represents the handler of connections.
    '''
    try:
        with filelock.FileLock('file.lock'):
            sock.settimeout(timeout.CONNECT)
            conn, address = sock.accept()
    except TimeoutError:
        return 1

    status = 0

    try:
        while True:
            conn.settimeout(timeout.COMMAND_RECV)
            args = conn.recv(length.COMMAND).decode().split()

            if args[0] == 'quit':
                break

            if args[0] == 'echo':
                command.echo(conn, args)
            elif args[0] == 'time':
                command.time(conn, args)
            elif args[0] == 'upload':
                command.upload(conn, args)
            elif args[0] == 'download':
                command.download(conn, args)
            else:
                command.unknown(conn)
    except TimeoutError:
        status = 1

    return status

def main():
    '''
    The main function of the program.
    '''
    global sock

    if len(sys.argv) != 3:
        print('usage: %s <address> <port>' % sys.argv[0], file=sys.stderr)
        sys.exit(1)

    address = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((address, port))
    sock.listen(N_MAX)

    proc.freeze_support()

    status = handle(sock)

    sock.close()

    sys.exit(status)

if __name__ == '__main__':
    main()
