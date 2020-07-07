#!usr/bin/python
# Author:   @BlankGodd_

import mod
import sys, socket

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = 4200

if __name__ == '__main__':
    while True:
        try:
            sock = socket.socket(socket.AF_INET, 
                    socket.SOCK_STREAM)
            print('Connecting to {}:{}'.format(HOST, PORT))
            sock.connect((HOST, PORT))
            print()
            print("Type message, enter to send, 'q' to quit")
            recvd = ''
            while recvd != 'c4':
                msg = input(': ')
                if msg == 'q': break
                mod.send_msg(sock,msg)
                for i in range(3):
                    try:
                        recvd = mod.recv_msg(sock)
                        print(recvd)
                        print()
                    except:
                        pass        
                if recvd == 'c4':
                    break
        except ConnectionError:
            print('Socket error')
            break
        finally:
            sock.close()
            print('Closed connection to server\n')


