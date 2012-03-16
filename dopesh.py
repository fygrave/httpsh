#!/usr/bin/env python

import socket, os, pexpect, string, sys, time

if len(sys.argv) != 2:
	print "usage ./dopesh.py socket file"
	sys.exit(1)
sock = sys.argv[1]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try: 
	os.remove(sock)
except OSError:
	pass

s.bind(sock)

s.listen(1)

def get_shell():
	return  pexpect.spawn("/bin/bash", env = {"TERM": "linux", "PS1":'[\d \t \u@\h:\w ] $'})

c = get_shell()

while 1:
	try:
		conn,addr = s.accept()
		conn.send("Connected\n")
		conn.setblocking(0)
	except:
		continue

	while 1:
		try:
			print "recv"
			data = conn.recv(1024)
			print "recv2"
			if  data: 

				if string.find(data,"sendcontrol") != -1 and (len(data) == (len("sendcontrol") + 1)):
					c.sendcontrol(data[len("sendcontrol")])
                		elif data != "null":
					c.sendline(data)
			if c.isalive() == False:
				c = get_shell()
			while c.expect([pexpect.TIMEOUT, pexpect.EOF, '.+'], timeout = 1) != 0:
				print "send"
				conn.send(c.before)
				print "send2"
				conn.send(c.after)
				print "send3"
		except Exception ,e:
			#print "Error Dopesh: ",str(e)
			time.sleep(0.5)
			pass
			#conn.close()
			#break




