#!/usr/bin/env python
import pytest
import echo_server
from threading import Thread
import socket


def dummy_client():
    message = "Christian Bale is a terrible actor."
    port = 50000
    address = '127.0.0.1'
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    client_socket.connect((address, port))
    client_socket.sendall(message)
    client_socket.shutdown(socket.SHUT_WR)

    return client_socket.recv(1024)


def test_connection():
    thread = Thread(target=echo_server.main)
    thread.start()
    assert dummy_client() == "Christian Bale is a terrible actor."
