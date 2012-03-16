#!/usr/bin/env python

import atexit
import os
import readline
import rlcompleter
import sys
import threading
import sys
import urllib
import base64
import select
import time


HISTORY_FILE = "~/.pyshell_history"

if (len(sys.argv) < 2):
	print "usage %s url" % (sys.argv[0])
	exit(0) 

pollUrl = sys.argv[1]

print "Starting shell via %s" % (pollUrl)

## polling
def dopoll(args):
	url = args
	#print "url = ",url
	data = ''
	try:
		d = urllib.urlopen(url)
		data = d.read()
		sys.stdout.write(  base64.b64decode(data))
		sys.stdout.flush()
	except:
		pass



def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

# shell code
def saveHistory():
 historyPath = os.path.expanduser(HISTORY_FILE)
 readline.write_history_file(historyPath)


def loadHistory():
 historyPath = os.path.expanduser(HISTORY_FILE)

 if os.path.exists(historyPath):
     readline.read_history_file(historyPath)


class CompleterNG(rlcompleter.Completer):
 def global_matches(self, text):
     """
     Compute matches when text is a simple name.
     Return a list of all names currently defined
     in self.namespace that match.
     """

     matches = []
     n = len(text)

     for list in [ self.namespace ]:
         for word in list:
             if word[:n] == text:
                 matches.append(word)

     return matches


def autoCompletion():
 completer = CompleterNG({ "cmd1": None,
                           "cmd2": None, })

 readline.set_completer(completer.complete)
 readline.parse_and_bind("tab: complete")

 loadHistory()
 atexit.register(saveHistory)


if __name__ == "__main__":
 autoCompletion()

 while True:
     input = None

     try:
        time.sleep(1)
	if isData():
         	input = raw_input("")
		if not input:
        		input = '\n'
     except KeyboardInterrupt:
         sys.stderr.write("\nCaught CTRL+C\n")
         input = "sendcontrolc"
     except EOFError:
         sys.stderr.write("\nCaught CTRL+D.. if you want to quit: dopequit\n")
         input = "sendcontrold"

     if (input == "dopequit"):
	break

     #if input.lower() in ( "x", "q", "exit", "quit" ):
     #    break

     if (input):
     	urllib.quote(input)
     	dopoll( "%s?%s" %(pollUrl, urllib.quote(input)))
     else:
	dopoll(pollUrl)
