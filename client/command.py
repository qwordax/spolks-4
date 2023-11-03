import os
import socket
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
    sock.settimeout(timeout.COMMAND_RECV)

    if sock.recv(length.COMMAND).decode() == 'usage':
        print('usage: upload <file>', file=sys.stderr)
        return

    if not os.path.exists(args[1]):
        sock.settimeout(timeout.COMMAND_SEND)
        sock.send('not exists'.encode())

        print('error: \'%s\' does not exists' % args[1], file=sys.stderr)
        return
    else:
        sock.settimeout(timeout.COMMAND_SEND)
        sock.send('exists'.encode())

    file_name = args[1]
    file_size = os.path.getsize(args[1])

    file_info = file_name+' '+str(file_size)

    sock.settimeout(timeout.COMMAND_SEND)
    sock.send(file_info.encode())

    with open(file_name, 'rb') as file:
        i = 0
        oob = file_size // length.FILE

        size = 0
        oob_size = 0

        for data in iter(lambda: file.read(length.FILE), b''):
            if i < oob:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                sock.settimeout(timeout.FILE_SEND)
                sock.send(data)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)

                oob_size += len(data)
            else:
                sock.settimeout(timeout.FILE_SEND)
                sock.send(data)

                size += len(data)

            i += 1

def download(sock, args):
    '''
    Represents the handler of the `download` command.
    '''
    sock.settimeout(timeout.COMMAND_RECV)

    if sock.recv(length.COMMAND).decode() == 'usage':
        print('usage: download <file>', file=sys.stderr)
        return

    sock.settimeout(timeout.COMMAND_RECV)

    if sock.recv(length.COMMAND).decode() == 'not exists':
        print('error: \'%s\' does not exists' % args[1], file=sys.stderr)
        return

    sock.settimeout(timeout.COMMAND_RECV)
    file_info = sock.recv(length.COMMAND).decode().split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    with open(file_name, 'wb') as file:
        i = 0
        oob = file_size // length.FILE

        size = 0
        oob_size = 0

        while (size+oob_size) < file_size:
            if i < oob:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                sock.settimeout(timeout.FILE_RECV)
                oob_size += file.write(sock.recv(length.FILE))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                sock.settimeout(timeout.FILE_RECV)
                size += file.write(sock.recv(length.FILE))

            i += 1

def unknown(sock, args):
    '''
    Represents the handler of unknown commands.
    '''
    sock.settimeout(timeout.COMMAND_RECV)
    response = sock.recv(length.COMMAND).decode()

    if response == 'unknown':
        print(f'error: unknown command \'{" ".join(args)}\'', file=sys.stderr)
