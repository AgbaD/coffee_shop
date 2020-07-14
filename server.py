#!usr/bin/python
# Author:   @BlankGodd_

import select
import mod
from types import SimpleNamespace
from collections import deque

HOST = mod.HOST
PORT = mod.PORT

clients = {}

def create_client(sock):
    return SimpleNamespace(sock=sock,rest=bytes(),
                           send_queue=deque())

def broadcast_msg(msg):
    data = mod.prep_msg(msg)
    for client in clients.values():
        client.send_queue.append(data)
        poll.register(client.sock, select.POLLOUT)

if __name__ == '__main__':
    listen_sock = mod.create_listen_socket(HOST, PORT)
    poll = select.poll()
    poll.register(listen_sock, select.POLLIN)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))

    while True:
        for fd, event in poll.poll():
            if event & (select.POLLHUP | select.POLLERR |
                select.POLLNVAL):
                poll.unregister(fd)
                del clients[fd]
                
            elif fd == listen_sock.fileno():
                client_sock,addr = listen_sock.accept()
                client_sock.setblocking(False)
                fd = client_sock.fileno()
                clients[fd] = create_client(client_sock)
                poll.register(fd, select.POLLIN)
                print('Connection from {}'.format(addr))

            elif event & select.POLLIN:
                client = clients[fd]
                addr = client.sock.getpeername()
                recvd = client.sock.recv(4096)
                if not recvd:
                    client.sock.close()
                    print('Client {} disconnected'.format(addr))
                    continue
                data = client.rest + recvd
                (msgs, client.rest) = mod.parse_recvd_data(data)
                for msg in msgs:
                    msg = '{}: {}'.format(addr, msg)
                    print(msg)
                    broadcast_msg(msg)

            elif event & select.POLLOUT:
                client = clients[fd]
                data = client.send_queue.popleft()
                sent = client.sock.send(data)
                if sent < len(data):
                    client.sends.appendleft(data[sent:])
                if not client.send_queue:
                    poll.modify(client.sock, select.POLLIN)

