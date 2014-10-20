#!/usr/bin/env python
import socket, os
from httplib import responses
from datetime import datetime

def get_size(dirname):
    """Gets the total size of a given directory"""
    size = 0
    for item in os.listdir(dirname):
        if os.path.isfile(item):
            size += os.path.getsize(item)
        elif os.path.isdir(item):
            size += get_size(item)
    return size

def htmlize(drct):
    """Wraps content in html tags"""
    lst = []
    for item in os.listdir(drct):
        lst.append("<li>%s</li>"%item)
        content = ("\n").join(lst)
    return "<html>\n<body>\n<ul>\n{content}\n</ul>\n</body>\n</html>".format(content=content)

def parse_request(request):
    parsed = request.split("\r\n")   # <--- Splits the request by new lines so the init req and each header is seperated.
    return parsed                    #      We haven't been asked to do anything with request headers, so for now, if any are passed as
                                     #      as a part of the request, they will sit here.

def parse_init_req_line(req_line):
    """Takes an HTTP request in the form of a string and parses it. Returns a tuple containing
    the URI (or where it should be) and a status code: 200 if the parse was successful, 400/405
    if it was not. Takes the initial request line as argument"""
    if req_line[:3] != "GET":
        status = 405
        # # # Raise Error 405 # # #
    elif req_line[-8:] != "HTTP/1.1":
        status = 400
        # # # Raise Error 400 # # #
    else:
        status = 200
    return (req_line[3:-8].strip(), status)
    

def reqOK():
    """Returns HTTP '200 OK' response"""
    pass

def responseHeaders(h1, h2, h3):
    """Returns a dict of headers to be used in the response"""
    headers = {}
    headers['Content-Type'] = h1
    headers['Date'] = h2
    headers['Server'] = "ServerTron4000"
    headers['Content-Length'] = h3
    return headers

def buildResponse(init_line, hdrs, body):
    """Build the final response to be sent to the client. Status, headers and all"""
    line1 = init_line + "\r\n"
    header_block = []
    for k, v in hdrs.items():
        header_block.append("%s:  %s"%(k,v))
    headers = ("\r\n").join(header_block)
    bodylines = "\r\n\r\n" + body
    return line1 + headers + bodylines + "\r\n\r\n"

def raiseResponse(status_code):
    """Raise appropriate status response. Makes use of httplib.responses"""
    return "%s %s" % (status_code, responses[status_code])

def getResource(uri):
    """Takes URI as argument; returns a tuple containing the content_type, the content_length, the resource requested as the body, and the status code, in that order"""
    body = ""                                       #
    content_type = ""                               # <--- Initialize the variables to hold the body and headers. For clarity.
    content_length = 0                              #
    type_dict = {'txt':'text', 'html':'text', 'py':'text', 'jpg':'image', 'png':'image'}
    status = 200
    if os.path.exists(uri):                         # <--- If the resource exists, return a body and Headers appropriate to the request.
        if os.path.isfile(uri):                     # <--- If the resource is a file:
            content_length = os.path.getsize(uri)   # <--- Determine its size...
            subtype =  uri.split('.')[-1]           # <--- Grab the extension...
            content_type = "%s/%s" % (type_dict[subtype], subtype)  # <--- Determine content type from file extension, and finally...
            with open(uri, 'rb') as f:              # <--- Open the file as binary data.
                while True:
                    readBytes = f.read(1024)
                    body += readBytes               # <--- Writes contents of file to a string.
                    if readBytes == "":
                        break
        elif os.path.isdir(uri):   # <--- If the resource is a directory:
            content_type = 'text/directory'
            content_length = get_size(uri)   # <--- Gets the size of the directory--the sum of the size of all files and subdirectories.  Maybe the content_length for a directory should just be the length of the content actually displayed...idk.
            body = htmlize(uri)
    else:
        status = 404

    return (content_type, str(content_length), body, status)


def Main():
    pass
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
        
        next = conn.recv(1024)
        request = next
        while next != "\r\n":      # <--- If I want to be able to send a body in with the request (which is seperateted
            next = conn.recv(1024) #      from the initial request line and headers with a blank line, then just re-write
            request += next        #      this condition to be 'while "\r\n\r\n" not in request:...'
        
        request = parse_request(request)  # <--- Now my request is split into chunks: Init line, header1, header2...
        result = parse_init_req_line(request[0])  # <--- tuple of (URI, status code) from init request line 
        uri = result[0]
        status = result[1]
        if status != 200:          # <--- If the URI was not parsed correctly, prepare an appropriate response
            init_response_line = "HTTP/1.1 %s" % raiseResponse(status)
            b1 = "Error 405. Only the GET method is supported by this server."
            b2 = "Error 400. Only HTTP version 1.1 is supported by this server."
            response_body = b1 if status == 405 else b2
            headers = responseHeaders('text/html', datetime.now(), len(response_body))
            response = buildResponse(init_response_line, headers, response_body)
            conn.sendall(response)
            conn.shutdown(socket.SHUT_WR)
            conn.close()
        else:

    s.close()

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

if __name__ == '__main__':
    Main()
