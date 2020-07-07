#!usr/bin/python
# Author:   @BlankGodd_

import socket
import ast
import threading
import mod

HOST = ''
PORT = 4200

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(100)

addr = sock.getsockname()
print('Listening on {}'.format(addr))
print()

while True:
    client_sock, addr = sock.accept()
    thread = threading.Thread(target=mod.handle_client,
                              args=[client_sock,addr],
                              daemon=True)
    thread.start()
    print('Connection from {}'.format(addr))


