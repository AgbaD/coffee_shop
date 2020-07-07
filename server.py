#!usr/bin/python
# Author:   @BlankGodd_

import socket
import ast
import threading

HOST = ''
PORT = 4200

listt = [
        ('caffe americano', 'cafe latte', 'cappuccino', 
        'espresso', 'long black', 'cupcakes', 'doughnuts', 
        'scones', 'cookies'), 
        
        (700, 550, 850, 600, 500, 300, 250, 300, 200)
        ]

cur_cli = []

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
    return msg.lower()

def send_msg(sock,msg):
    msg += '\0'
    data = msg.encode('utf-8')
    sock.sendall(data)

def converse(sock,addr):
    while True:
        msg = recv_msg(sock)
        print('{}: {}'.fromat(addr, msg))
        print()
        if msg in listt[0]:
            send_msg(sock,'Confirmed Payment(y/n)')
            conf = recv_msg(sock)
            if conf == 'y':
                send_msg(sock,'Payment Confirmed')
                send_msg(sock,'Order Complete')
            else:
                send_msg(sock,'Order Canceled')
                break
        else:
            send_msg(sock,'Order not recognised')
            send_msg(sock,'Place new order')
            converse(sock, addr)

def handle_client(sock, addr):
    if addr in cur_cli:
        pass
    else:
        cur_cli.append(addr)
        send_msg(sock,"Welcome to Coffee Shop!")
        send_msg(sock,'What do you want to buy')
        send_msg(sock,'Enter order name as listed')
        send_msg(sock,"")
        for i in range(9):
            send_msg(sock,listt[0][i],'\t',listt[1][i])
    try:
        converse(sock,addr)
    except (ConnectionError, BrokenPipeError):
        print('Socket Error')
    finally:
        print('Closed connection to {}'.format(addr))
        cur_cli.remove(addr)
        sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(100)

addr = sock.getsockname()
print('Listening on {}'.format(addr))
print()

while True:
    client_sock, addr = sock.accept()
    thread = threading.Thread(target=handle_client,
                              args=[client_sock,addr],
                              daemon=True)
    thread.start()
    print('Connection from {}'.format(addr))


