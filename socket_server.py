#!/usr/bin/env python
# make use of httplib.responses()
import socket
from datetime import datetime

def req_ok(content):
    time= datetime.now()
    length= len(bytearray(content))
    response= "HTTP/1.1 200 OK\r\nDate: {t}\r\nContent-Length: {l}\r\n\r\n".format(t=time, l=length)
    return bytearray(response)

def req_notok(content):
    return bytearray("HTTP/1.1 400 Bad Request")

def parse_uri(request):
    if request[:3] != 'GET': 
        return -1
    elif request[-10:-2] != 'HTTP/1.1':
        return -2
    else:
        return bytearray(request[4:-9])

def Main():
    port= 50000
    address= '127.0.0.1'
    print "\nSocket server starting...\n"
    s= socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    s.bind((address, port))
    s.listen(1)
    conn, client_addr= s.accept()
    request= str(conn.recv(1024))

    if parse_uri(request)== -1:
        message= bytearray('Bad Request. Must be of the form GET\n')
    elif parse_uri(request)== -2:
        message= bytearray('Bad Request. HTTP protocol must be 1.1\n')
    else:
        message= req_ok(request)

    conn.sendall(message)

    conn.shutdown(socket.SHUT_WR)
    conn.close()
    s.close()


if __name__ == '__main__':
    Main()
