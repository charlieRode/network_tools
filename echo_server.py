#!/usr/bin/env python
import socket


def main():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    msg = conn.recv(1024)
    conn.sendall(msg)
    conn.shutdown(socket.SHUT_WR)
    conn.close()

if __name__ == '__main__':
    main()
