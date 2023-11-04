import filelock

import logging as log
import multiprocessing as proc
import socket
import sys

import command
import length
import timeout

N_MIN = 2
'''
The minimum number of processes.
'''

N_MAX = 5
'''
The maximum number of processes.
'''

def handle(sock, count, status, working):
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
        except KeyboardInterrupt:
            return

    status.value += 1
    log.info('%s:%d connected' % address)

    try:
        while True:
            conn.settimeout(timeout.COMMAND_RECV)
            args = conn.recv(length.COMMAND).decode().split()

            if args[0] == 'close':
                working.value = 0
                break

            if args[0] == 'quit':
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
    except ConnectionAbortedError:
        log.error('%s:%d connection aborted' % address)
    except ConnectionResetError:
        log.error('%s:%d connection reset' % address)
    except TimeoutError:
        log.error('%s:%d timeout expired' % address)

    count.value -= 1
    status.value -= 1

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
    sock.listen(1)

    # Necessary for properly process executing.
    proc.freeze_support()

    # Indicates total number of processes.
    count = proc.Value('b', 0)

    # Indicates total number of working processes.
    status = proc.Value('b', 0)

    # Indicates server working.
    working = proc.Value('b', 1)

    # The list of processes that handle connections.
    process_list = []

    try:
        while working.value:
            if ((count.value < N_MIN or count.value == status.value) and
                 count.value < N_MAX):
                process_list.append(proc.Process(
                    target=handle,
                    args=(sock.dup(), count, status, working)
                ))

                process_list[-1].start()

                count.value += 1
                log.info('start process')
    except KeyboardInterrupt:
        log.critical('interrupt')

    # Terminating processes.
    for p in process_list:
        if p.is_alive():
            p.terminate()
            log.info('terminate process')

            p.join()

    log.info('closing . . .')
    sock.close()

    sys.exit(0)

if __name__ == '__main__':
    main()
