# Pidfile module

# Use: 
# Call pidfile.use(option=value) in the beginning of your script
#
# Options:
#
# continue_on_error
#	Continue if we find a "zombie" pidfile; if False then sys.exit(1)
# 	Default True
# pidfilePath
#	Set the path in which to store/look for pidfiles
#	Default "/tmp/"

# Jeff Casavant 06/03/2014

import os
import sys
import pwd
import atexit

# Location of pidfile
pidfilePath = "/tmp/"
pidfile = pidfilePath + sys.argv[0] + ".pid"
pid = str(os.getpid())

# Function to be called externally
def use(continue_on_error=True, pidfilePath="/tmp/"):
	
	pidfile = pidfilePath + sys.argv[0] + ".pid"
	
	if not os.access(pidfile, os.R_OK):
		_create_pidfile()
	else:
		if _running():
			print "%s already running!" % sys.argv[0] 
			sys.exit(1)
		else:
			print "Previous %s left pidfile (terminated unexpectedly)!" % sys.argv[0]
			os.remove(pidfile)
			if continue_on_error:
				_create_pidfile()
			else:
				sys.exit(1)

def _create_pidfile():
	try:
		pf = open(pidfile, 'w')
		os.chmod(pidfile, 0644)
		pf.write(pid)
		pf.close()
		# Delete pidfile on exit()
		atexit.register(_exit)
	except Exception, e:
		if os.path.exists(pidfile):
			uid = os.stat(pidfile).st_uid
			name = pwd.getpwuid(uid)
			print "Could not write to %s: file exists, owned by UID %s %s" % (pidfile, uid, name)
		else:
			print "Could not write to %s" % pidfile


def _running():
	pf = open(pidfile, 'r')
	pid = pf.read()
	pf.close()
	return os.path.exists("/proc/" + pid)

def _exit():
	if not _running():
		os.remove(pidfile)