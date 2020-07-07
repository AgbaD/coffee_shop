#!usr/bin/python
# Author:   @BlankGodd_

import socket
import sys
import threading

HOST = ''
PORT = 4200

def connect_soc(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return soc

def process_msg(msg):
    
