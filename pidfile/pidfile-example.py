#!/usr/bin/env python

# Example of the use of a pidfile

import sys

import pidfile

# For simulation purposes only
from time import sleep

pidfile.use()

# Simulate processing
sleep(15)

sys.exit(0)