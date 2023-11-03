import logging as log
import os
import socket
import time as ctime

import length
import timeout

def echo(conn, address, args):
    '''
    Represents the handler of the `echo` command.
    '''
    log.info('%s:%d %s' % (address + (' '.join(args),)))

    conn.settimeout(timeout.COMMAND_SEND)
    conn.send(('\n'.join(args[1:])+'\n').encode())

def time(conn, address, args):
    '''
    Represents the handler of the `time` command.
    '''
    log.info('%s:%d %s' % (address + (' '.join(args),)))

    if len(args) != 1:
        response = 'usage'
    else:
        response = ctime.ctime()

    conn.settimeout(timeout.COMMAND_SEND)
    conn.send(response.encode())

def upload(conn, address, args):
    '''
    Represents the handler of the `upload` command.
    '''
    log.info('%s:%d %s' % (address + (' '.join(args),)))

    if len(args) != 2:
        conn.settimeout(timeout.COMMAND_SEND)
        conn.send('usage'.encode())
    else:
        conn.settimeout(timeout.COMMAND_SEND)
        conn.send('ok'.encode())

    conn.settimeout(timeout.COMMAND_RECV)

    if conn.recv(length.COMMAND).decode() == 'not exists':
        return

    conn.settimeout(timeout.COMMAND_RECV)
    file_info = conn.recv(length.COMMAND).decode().split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    with open(file_name, 'wb') as file:
        i = 0
        oob = file_size//length.FILE // 4

        size = 0
        oob_size = 0

        while (size+oob_size) < file_size:
            if i < oob:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                conn.settimeout(timeout.FILE_RECV)
                oob_size += file.write(conn.recv(length.FILE))
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                conn.settimeout(timeout.FILE_RECV)
                size += file.write(conn.recv(length.FILE))

            if i%length.FILE == 0:
                log.info(f'{int(100 * (size+oob_size) / file_size):3d} %')

            i += 1

        log.info(f'received {size:,.0f} + {oob_size:,.0f} bytes')

def download(conn, address, args):
    '''
    Represents the handler of the `download` command.
    '''
    log.info('%s:%d %s' % (address + (' '.join(args),)))

    if len(args) != 2:
        conn.settimeout(timeout.COMMAND_SEND)
        conn.send('usage'.encode())

        return
    else:
        conn.settimeout(timeout.COMMAND_SEND)
        conn.send('ok'.encode())

    if not os.path.exists(args[1]):
        conn.settimeout(timeout.COMMAND_SEND)
        conn.send('not exists'.encode())

        return
    else:
        conn.settimeout(timeout.COMMAND_SEND)
        conn.send('exists'.encode())

    file_name = args[1]
    file_size = os.path.getsize(args[1])

    file_info = file_name+' '+str(file_size)

    conn.settimeout(timeout.COMMAND_SEND)
    conn.send(file_info.encode())

    with open(file_name, 'rb') as file:
        i = 0
        oob = file_size//length.FILE // 4

        size = 0
        oob_size = 0

        for data in iter(lambda: file.read(length.FILE), b''):
            if i < oob:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                conn.settimeout(timeout.FILE_SEND)
                conn.send(data)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)

                oob_size += len(data)
            else:
                conn.settimeout(timeout.FILE_SEND)
                conn.send(data)

                size += len(data)

            if i%length.FILE == 0:
                log.info(f'{int(100 * (size+oob_size) / file_size):3d} %')

            i += 1

        log.info(f'sent {size:,.0f} + {oob_size:,.0f} bytes')

def unknown(conn, address, args):
    '''
    Represents the handler of unknown commands.
    '''
    log.warning('%s:%d %s' % (address + (' '.join(args),)))

    conn.settimeout(timeout.COMMAND_SEND)
    conn.send('unknown'.encode())
