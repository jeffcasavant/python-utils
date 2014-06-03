#!/usr/bin/env python

# Example of the use of a pidfile

# Notes: be sure to os.remove(pidfile) before any calls to sys.exit() that fall
# inside the if statement; there should only be one sys.exit() without a matching
# os.remove(pidfile), and that is in the else clause that throws an error b/c 
# the script is currently running

import sys

import pidfile

# For simulation purposes only
from time import sleep

pidfile.use()

# Simulate processing
sleep(15)

sys.exit(0)