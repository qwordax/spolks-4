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
    pass

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

def unknown(conn, args):
    '''
    Represents the unknown command handler.
    '''
    pass
