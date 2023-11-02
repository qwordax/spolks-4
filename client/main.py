import atexit
import socket
import sys

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

    while True:
        args = input('> ').split()

        if args == []:
            continue

        if args[0] == 'quit':
            break

if __name__ == '__main__':
    main()
