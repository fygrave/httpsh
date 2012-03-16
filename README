
this is multi-user shell-over-http tool
=======================================


General artichitecture:

dopec.py --> talks to web server -> runs proxy code -> talks to  dopesrv -> launches dopesh.py for every session.

STARTING:

2. you start http server as ./dopesrv.py - being in current folder is important (PWD this is), because this is where we will look for dopesh.py

3. for each /<sessionID>?commands (or /<sessionID>) http server will launch a new dopesh.py with socket /tmp/dopesock.<sessionID> (woow.. you can own me! ;-))

number of sessions is unlimited

there is no way to "kill session"

4.  dopesh.py gets launched automagically.



Other languages contain scripts in other languages, so you can proxy requests to our shell.
