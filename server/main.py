import atexit
import socket
import sys

N_MIN = 1
'''
The minimum number of threads.
'''

N_MAX = 3
'''
The maximum number of threads.
'''

def handle():
    '''
    Represents the handler of the connection.
    '''
    pass

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

    sock.bind((address, port))
    sock.listen(N_MAX)

if __name__ == '__main__':
    main()
