import sys

import timeout

def echo(sock):
    '''
    Represents the `echo` command handler.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    print(sock.recv(1024).decode())

def time(sock):
    '''
    Represents the `time` command handler.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    response = sock.recv(1024).decode()

    if response == 'usage':
        print('usage: time', sys.stderr)
    else:
        print(response)

def upload(sock, args):
    '''
    Represents the `upload` command handler.
    '''
    pass

def download(sock, args):
    '''
    Represents the `download` command handler.
    '''
    pass

def unknown(sock, args):
    '''
    Represents the unknown command handler.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    response = sock.recv(1024).decode()

    if response == 'unknown':
        print(f'error: unknown command \'{" ".join(args)}\'', file=sys.stderr)
