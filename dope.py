#!/usr/bin/env python

import pexpect, socket


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

s.connect("/tmp/dopesock")

c = pexpect.spawn("/bin/bash")
c.expect([pexpect.TIMEOUT, pexpect.EOF, '\$'])

s.send(c.before)
s.send(c.after)
done = False
while ( ! done):
	data = s.recv(1024)
	c.sendline(data)
	while c.expect([pexpect.TIMEOUT, pexpect.EOF, '.+'], timeout = 1) != 0:
		s.send(c.before)
		s.send(c.after)




