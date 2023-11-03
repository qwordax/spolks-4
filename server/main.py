import filelock

import logging as log
import multiprocessing as proc
import socket
import sys
import time

import command
import length
import timeout

N_MIN = 3
'''
The minimum number of threads.
'''

N_MAX = 5
'''
The maximum number of threads.
'''

DELAY = 0.5
'''

'''

def handle(sock, working):
    '''
    Represents the handler of connections.
    '''
    # Logging configuration.
    log.basicConfig(
        level=log.INFO,
        format='%(levelname)-8s | %(message)s'
    )

    while True:
        try:
            with filelock.FileLock('file.lock'):
                log.info('accepting . . .')

                sock.settimeout(timeout.CONNECT)
                conn, address = sock.accept()

                break
        except TimeoutError:
            log.warning('timeout expired')

    log.info('%s:%d connected' % address)

    try:
        while True:
            conn.settimeout(timeout.COMMAND_RECV)
            args = conn.recv(length.COMMAND).decode().split()

            if args[0] == 'quit':
                working.value = 0
                break

            if args[0] == 'echo':
                command.echo(conn, address, args)
            elif args[0] == 'time':
                command.time(conn, address, args)
            elif args[0] == 'upload':
                command.upload(conn, address, args)
            elif args[0] == 'download':
                command.download(conn, address, args)
            else:
                command.unknown(conn, address, args)
    except ConnectionResetError:
        log.error('%s:%d connection reset' % address)
    except TimeoutError:
        log.error('%s:%d timeout expired' % address)

    log.info('%s:%d disconnected' % address)

def main():
    '''
    The main function of the program.
    '''
    global sock

    # Logging configuration.
    log.basicConfig(
        level=log.INFO,
        format='%(levelname)-8s | %(message)s'
    )

    if len(sys.argv) != 3:
        print('usage: %s <address> <port>' % sys.argv[0], file=sys.stderr)
        sys.exit(1)

    address = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((address, port))
    sock.listen(N_MAX)

    # Necessary for processes to work properly.
    proc.freeze_support()

    # Shared variable to indicate server working.
    working = proc.Value('b', 1)

    # The list of processes that handle connections.
    process_list = []

    for _ in range(N_MIN):
        process_list.append(proc.Process(
            target=handle,
            args=(sock.dup(), working)
        ))

    for p in process_list:
        p.start()
        log.info('start process')

    try:
        while working.value:
            time.sleep(DELAY)
    except KeyboardInterrupt:
        log.critical('interrupt')

    # Terminating processes.
    for p in process_list:
        p.terminate()
        p.join()

    log.info('closing . . .')
    sock.close()

    sys.exit(0)

if __name__ == '__main__':
    main()
