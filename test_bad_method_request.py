#!/usr/bin/env python
import socket_server, pytest, socket

address= ('127.0.0.1', 50000)
tester_client= socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)

def test_bad_method_request():
    request= "HEAD www.wombatlyfe.com HTTP/1.1\r\n"
    tester_client.connect(address)
    tester_client.sendall(request)
    message= tester_client.recv(1032)
    tester_client.shutdown(socket.SHUT_WR)
    tester_client.close()

    assert 'Bad Request. Must be of the form GET' in message
