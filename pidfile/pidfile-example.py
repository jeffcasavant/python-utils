#!/usr/bin/env python

# Example of the use of a pidfile

import sys

# For simulation purposes only
from time import sleep

import pidfile

pidfile.use(continueOnError=False)

# Simulate processing
sleep(15)

sys.exit(0)