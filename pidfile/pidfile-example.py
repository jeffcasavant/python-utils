#!/usr/bin/env python

# Example of the use of a pidfile

import sys

# For simulation purposes only
from time import sleep

import pidfile

pidfile.use()

# Simulate processing
#sleep(5)

print pidfile._owner_info(pidfile.pidfile)

sys.exit(0)