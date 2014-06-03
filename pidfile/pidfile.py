# Pidfile module

import os
import sys
import atexit

# Location of pidfile
pidfilePath = "/tmp/"
pidfile = pidfilePath + sys.argv[0] + ".pid"
pid = str(os.getpid())

def use(allow_duplicates=False, continue_on_error=True):
	if not os.path.exists(pidfile):
		create_pidfile()
	else:
		if running():
			print "%s already running!" % sys.argv[0]
			if not allow_duplicates:
				sys.exit(1)
		else:
			print "Previous %s left pidfile - probably terminated unexpectedly!" % sys.argv[0]
			os.remove(pidfile)
			if continue_on_error:
				create_pidfile()
			else:
				sys.exit(1)

def create_pidfile():
	pf = open(pidfile, 'w')
	pf.write(pid)
	pf.close()
	# Delete pidfile on sys.exit()
	atexit.register(exit)

def running():
	pf = open(pidfile, 'r')
	pid = pf.read()
	pf.close()
	return os.path.exists("/proc/" + pid)

def exit():
	if not running():
		os.remove(pidfile)