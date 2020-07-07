#!usr/bin/python
# Author:   @BlankGodd_

import socket
import ast
import threading

HOST = ''
PORT = 4200

with open('store.txt','r') as store:
    listt = ast.literal_eval(store.read())

def recv_msg(sock):
    data = bytearray()
    msg = ''
    while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            raise ConnectionError()
        data = data + recvd
        if b'\0' in recvd:
            msg = data.rstrip(b'\0')
    msg = msg.decode('utf-8')
    return msg

def handle_client(client_sock, addr):


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(100)

addr = sock.getsockname()
print('Listening on {}'.format(addr))

while True:
    client_sock, addr = sock.accept()
    thread = threading.Thread(target=handle_client,
                              args=[client_sock,addr],
                              daemon=True)





