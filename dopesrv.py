#!/usr/bin/env python
import time
import BaseHTTPServer
import socket
import string
import urllib
import base64
import os

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8993
MAX_BUFF_SIZE = 10000


def do_spawn(chan):
	if os.fork() == 0:
		os.execvp("./dopesh.py", ["./dopesh.py", chan])

def getdopesock(chan):
	while 1:
	    try:
		dopesock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		dopesock.setblocking(0)
		dopesock.connect("/tmp/dopesock." + chan)
		dopesock.send("whoami\n")
		break
	    except Exception, e:
		print str(e)
		do_spawn("/tmp/dopesock." + chan)
		time.sleep(1)
		pass

	return dopesock

dopesock = {}
dopebuf = ""

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
	global dopebuf
	global dopesock
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

	# get channel first
	key = s.path[1]
	print "channel ", key
	if not dopesock.has_key(key):
		dopesock[key] = getdopesock(key)
	# first see if we get keyboard input
        if string.find(s.path, "?") != -1:
		offset = string.find(s.path, "?") + 1
		try:
        		dopesock[key].send(urllib.unquote(s.path[offset:]))
		except Exception, e:
			dopesock[key] = getdopesock(key)
	# read data from socket
	# 	
        data = ""
        while 1:
           try:
             d = dopesock[key].recv(1024)
             data = data + d
           except Exception, e: # sockets are non-blocking. so we get exception when there is nothing to read
		break


	s.wfile.write(base64.encodestring(data))

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

