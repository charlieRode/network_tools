#!/usr/bin/env python
import socket, os

def parse_request(req):
    """Takes an HTTP request in the form of a string and parses it, returning the URI,
    if the request is valid"""
    pass

def reqOK():
    """Returns HTTP '200 OK' response"""
    pass

def reqERR():
    """Returns HTTP error response. Makes use of the module httplib.responses()"""
    pass

def getResource(uri):
    """Takes URI as argument; returns resource requested as a body and headers indicating the type of content in the body"""
    body = ""
    if os.path.exists(uri):  # <--- If the resource exists, return a body and Headers appropriate to the request.
        if os.path.isfile(uri):  # <--- If the resource is a file... 
            with open(uri, 'rb') as f:  # <--- Open it as binary data
                while True:
                    readBytes = f.read(1024)
                    body += readBytes
                    if readBytes == "":
                        break
    return body



    # else:  # <--- If the resource does not exist, return an Error message... (as the body of the response?)


def Main():
    """Here will be the main functionality of the server. We will build sockets, establish connections,
    listen for requests and return responses"""
    host, port = '127.0.0.1', 5000
    s = socket.socket()  # <--- May need to provide parameters... Unsure wheather the provided parameters are defaulted to.
    s.bind((host, port))
    s.listen(1)          # <--- May need to change this parameter. Takes values 0 thru 5.
    print "Server Started\nListening..."

    while True:          # <--- Not yet sure of the significance of this loop. Does it keep the server open and listening for new requests?
        conn, addr = s.accept()
        print "Client connected from ip: <%s>" % str(addr)
        # # # Here we might need to implement a thread to do our bidding while the server listens for requests # # #
        
        request = str(conn.recv(1024))
        # # # From here we will need to handle the request using the above defined functions! # # #
        #
        # # # First, we will parse the request to determine if it is valid. If it is, we will # # #
        #     extract the URI from the request and return it. If it is not valid, we will call
        #     upon our reqERR() function to raise the appropriate error message.
        #
        # # # Then, we will pass the URI to our getResource() function, which will return the # # #
        #     requested resource as a body, along with Headers that properly identify the 
        #     contents of the resource (e.g., text/html or image/gif.)
        #
        # # # Finally, the data returned from getResource() will be packaged with an HTTP     # # #
        #     "200 OK" response which we will send back through the socket

