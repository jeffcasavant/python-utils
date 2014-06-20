#!/usr/bin/env python

import argparse
# Import graphviz-python
from graphviz import Digraph
from time import sleep

###########
## Cmd-line args

parser = argparse.ArgumentParser(
	description='Draw Sam\'s Collatz plot to a given number.')

parser.add_argument('-m', '--max', type=int, metavar='N', 
	help='Number to stop at. (N>=1)')

parser.add_argument('-6', '--skip6', action='store_true', default=False,
	help='Skip numbers divisible by 6.')

parser.add_argument('-i', '--interval', type=int, help='Output interval')

parser.add_argument('-c', '--continuous', action='store_true', default=False,
	help='Continous')

parser.add_argument('-s', '--sleep', type=int, help='Sleep interval')

parser.add_argument('-o', '--out', help='Output filename', required=True)

args = parser.parse_args()

##########
## Globals
nodes = []

##########
## Return next number in Collatz sequence

def collatz_draw(n):
	if not args.skip6 or n % 6:
		if not n in nodes:
			graph.node('%d' % n, '%d' % n)
			nodes.append(n)
			if n % 2:
				nextN = 3 * n + 1
			else:
				nextN = n / 2
			collatz_draw(nextN)
			graph.edge('%d' % n, '%d' % nextN)

############
## Main

graph = Digraph()

n = 1
while args.continuous:
	print('Working on %d...' % n)
	collatz_draw(n)
	if not n % args.write_interval:
		print('Writing DOT for %d...' % n)
		with open(args.out + '%s' % n) as dotfile:
			dotfile.write(graph.source)
	if not n % args.sleep:
		print('Sleeping to avoid overload.')
		sleep(5)
	n += 1

for n in range(1, args.max + 1):
	print('Working on %d...' % n)
	collatz_draw(n)
	if not n % args.write_interval:
		print('Writing DOT for %d...' % n)
		with open(args.out + '%s' % n) as dotfile:
			dotfile.write(graph.source)
	if not n % args.sleep:
		print('Sleeping to avoid overload.')
		sleep(5)