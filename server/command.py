import time

def echo(conn, args):
    '''
    Represents an `echo` command handler.
    '''
    conn.settimeout(1)
    conn.send(('\n'.join(args[1:])+'\n').encode())

def time(conn, args):
    '''
    Represents a `time` command handler.
    '''
    if len(args) != 1:
        response = 'usage'
    else:
        response = time.ctime()

    conn.settimeout(1)
    conn.send(response.encode())

def upload(conn, args):
    '''
    Represents an `upload` command handler.
    '''
    pass

def download(conn, args):
    '''
    Represents a `download` command handler.
    '''
    pass

def unknown(conn):
    '''
    Represents an unknown command handler.
    '''
    conn.settimeout(1)
    conn.send('unknown'.encode())
