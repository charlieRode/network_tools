#!/usr/bin/env python
import socket, sys

message= sys.argv[1]
port= 50000
address= '127.0.0.1'

client_socket= socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)
client_socket.connect((address, port))
client_socket.sendall(message)
client_socket.shutdown(socket.SHUT_WR)

msg= client_socket.recv(1024)

print msg