import time

def echo(conn, args):
    '''
    Represents the `echo` command handler.
    '''
    conn.settimeout(1)
    conn.send(('\n'.join(args[1:])).encode())

def time(conn, args):
    '''
    Represents the `time` command handler.
    '''
    if len(args) != 1:
        response = 'usage'
    else:
        response = time.ctime()

    conn.settimeout(1)
    conn.send(response.encode())

def upload(conn, args):
    '''
    Represents the `upload` command handler.
    '''
    pass

def download(conn, args):
    '''
    Represents the `download` command handler.
    '''
    pass

def unknown(conn):
    '''
    Represents the unknown command handler.
    '''
    conn.settimeout(1)
    conn.send('unknown'.encode())
