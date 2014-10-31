#!/usr/bin/env python
import pytest
from http_server import parse_request, parse_init_req_line, responseHeaders, buildResponse, raiseResponse, getResource

good_request = "GET webroot/images/Sample_Scene_Balls.jpg HTTP/1.1\r\nHeader1: I don't really get what goes into a request header."
bad_method_call = "GIT webroot/sample.txt HTTP/1.1\r\nHeader1: Providing header data as part of an http request is called giving head."
bad_http_version = "GET funWithThreads.py HTTP/1.0\r\nHeader1: No one is reading my ridiculous test files, I assume."
nonsense = "Groop doopery dupe. Skadoosh!"

def test_good_request():
    x = parse_request(good_request)[0]
    assert x == "GET webroot/images/Sample_Scene_Balls.jpg HTTP/1.1"
    assert parse_init_req_line(x)[0] == "webroot/images/Sample_Scene_Balls.jpg"
    assert parse_init_req_line(x)[1] == 200

def test_405():
    x = parse_request(bad_method_call)[0]
    assert x == "GIT webroot/sample.txt HTTP/1.1"
    assert parse_init_req_line(x)[0] == "webroot/sample.txt"
    assert parse_init_req_line(x)[1] == 405

def test_400():
    x = parse_request(bad_http_version)[0]
    assert x == "GET funWithThreads.py HTTP/1.0"
    assert parse_init_req_line(x)[0] == "funWithThreads.py"
    assert parse_init_req_line(x)[1] == 400

def test_responseHeaders():
    h = responseHeaders('type', 'now', '1 million')
    assert h['Content-Type'] == 'type'
    assert h['Date'] == 'now'
    assert h['Server'] == 'ServerTron4000'
    assert h['Content-Length'] == '1 million'

def test_buildResponse():
    uri = parse_init_req_line(parse_request(good_request)[0])[0]
    b = getResource(uri)[2]
    h = responseHeaders(getResource(uri)[0], 'Today', getResource(uri)[1])
    response = buildResponse("HTTP/1.1 "+str(getResource(uri)[3])+" OK", h, b)
    assert "HTTP/1.1 200 OK" in response
    assert "image/jpg" in response
    assert "Requested resource is an image. Here is it's binary data vomit:" in response
