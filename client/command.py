import sys

import length
import timeout

def echo(sock):
    '''
    Represents the handler of the `echo` command.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    print(sock.recv(length.COMMAND).decode(), end='')

def time(sock):
    '''
    Represents the handler of the `time` command.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    response = sock.recv(length.COMMAND).decode()

    if response == 'usage':
        print('usage: time', file=sys.stderr)
    else:
        print(response)

def upload(sock, args):
    '''
    Represents the handler of the `upload` command.
    '''
    pass

def download(sock, args):
    '''
    Represents the handler of the `download` command.
    '''
    pass

def unknown(sock, args):
    '''
    Represents the handler of unknown commands.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    response = sock.recv(length.COMMAND).decode()

    if response == 'unknown':
        print(f'error: unknown command \'{" ".join(args)}\'', file=sys.stderr)
