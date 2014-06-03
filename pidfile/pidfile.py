# Pidfile module

# Use: 
# Call pidfile.use() in the beginning of your script
#
# Options:
# allow_duplicates 
#	Allow multiple instances of the same script
#	Default False
#
# continue_on_error
#	Continue if we find a "zombie" pidfile; if False then sys.exit(1)
# 	Default True

import os
import sys
import atexit

# Location of pidfile
pidfilePath = "/tmp/"
pidfile = pidfilePath + sys.argv[0] + ".pid"
pid = str(os.getpid())

# Function to be called externally
def use(allow_duplicates=False, continue_on_error=True):
	if not os.path.exists(pidfile):
		_create_pidfile()
	else:
		if _running():
			print "%s already running!" % sys.argv[0]
			if not allow_duplicates:
				sys.exit(1)
		else:
			print "Previous %s left pidfile - probably terminated unexpectedly!" % sys.argv[0]
			os.remove(pidfile)
			if continue_on_error:
				_create_pidfile()
			else:
				sys.exit(1)

def _create_pidfile():
	pf = open(pidfile, 'w')
	pf.write(pid)
	pf.close()
	# Delete pidfile on exit()
	atexit.register(_exit)

def _running():
	pf = open(pidfile, 'r')
	pid = pf.read()
	pf.close()
	return os.path.exists("/proc/" + pid)

def _exit():
	if not _running():
		os.remove(pidfile)