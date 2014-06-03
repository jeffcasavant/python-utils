#!/usr/bin/env python

# Example of the use of a pidfile

# Notes: be sure to os.remove(pidfile) before any calls to sys.exit() that fall
# inside the if statement; there should only be one sys.exit() without a matching
# os.remove(pidfile), and that is in the else clause that throws an error b/c 
# the script is currently running

import os
import sys

# For simulation purposes only
from time import sleep

# Location of pidfile
pidfilePath = "/tmp/"
pidfile = pidfilePath + sys.argv[0] + ".pid"
pid = str(os.getpid())

if not os.path.exists(pidfile):
	pf = open(pidfile, 'w')
	pf.write(pid)
	pf.close()

	# Do processing

	# Catch Exception, e:
		# handling
		# os.remove(pidfile)
		# sys.exit(1)

	sleep(15)

	os.remove(pidfile)
	sys.exit(0)

else:
	pf = open(pidfile, 'r')
	pid = pf.read()
	pf.close()
	if os.path.exists("/proc/" + pid):
		print "%s already running!" % sys.argv[0]
		sys.exit(1)
	else:
		print "Previous %s left pidfile! (probably terminated unexpectedly)" % sys.argv[0]
		os.remove(pidfile)
		sys.exit(1)
	