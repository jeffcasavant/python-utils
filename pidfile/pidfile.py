# Pidfile module

# Use: 
# Call pidfile.use(option=value) in the beginning of your script
#
# Options:
#
# continueOnError
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
def use(continueOnError=True, pidfilePath="/tmp/"):
	
	pidfile = pidfilePath + sys.argv[0] + ".pid"
	
	if not os.access(pidfile, os.R_OK):
		_create_pidfile()
	else:
		if _running():
			print "%s already running!" % sys.argv[0] 
			sys.exit(1)
		else:
			print "Previous %s left pidfile (terminated unexpectedly)!" % sys.argv[0]

			try:
				os.remove(pidfile)
			except Exception, e:
				info = _owner_info(pidfile)
				print "Could not remove %s: owned by UID %s '%s' with umask %s" % (pidfile, info['uid'], info['name'], info['umask'])

			if continueOnError:
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
			info = _owner_info(pidfile)
			print "Could not write to %s: file exists, owned by UID %s '%s' with umask %s" % (pidfile, info['uid'], info['name'], info['umask'])
		else:
			print "Could not write to %s" % pidfile


def _running():
	pf = open(pidfile, 'r')
	pid = pf.read()
	pf.close()
	return os.path.exists("/proc/" + pid)

def _owner_info(filepath):
	uid = os.stat(pidfile).st_uid
	name = pwd.getpwuid(uid)
	umask = os.umask(0)
	os.umask(umask)
	return {'uid' = uid, 'name' = name, 'umask' = umask)

def _exit():
	if not _running():
		os.remove(pidfile)