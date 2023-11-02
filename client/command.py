def echo(sock, args):
    '''
    Represents the `echo` command handler.
    '''
    sock.settimeout(1)
    print(sock.recv(1024).decode())

def time(sock, args):
    '''
    Represents the `time` command handler.
    '''
    pass

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
    pass
