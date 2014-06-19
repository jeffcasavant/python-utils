#!/usr/bin/env python

import argparse
# Import graphviz
from graphviz import Digraph
from time import sleep

###########
## Cmd-line args

parser = argparse.ArgumentParser(
	description='Draw Sam\'s Collatz plot to a given number.')

parser.add_argument('-m', '--max', type=int, metavar='N', 
	help='Number to stop at. (N>=1)', required=True)

parser.add_argument('-6', '--skip6', action='store_true', default=False,
	help='Skip numbers divisible by 6.')

parser.add_argument('-r', '--render', help='Render interval')

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

for n in range(1, args.max + 1):
	print('Working on %d...' % n)
	collatz_draw(n)
	if not n % args.render:
		print('Rendering for %d...' % n)
		graph.render(args.out)
	if not n % args.sleep:
		print('Sleeping to avoid overload.')
		sleep(5)

# Draw
graph.render(args.out)