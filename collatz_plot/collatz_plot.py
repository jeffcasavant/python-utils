#!/usr/bin/env python

import argparse
# Import graphviz
from graphviz import Digraph

###########
## Cmd-line args

parser = argparse.ArgumentParser(
	description='Draw Sam\'s Collatz plot to a given number.')

parser.add_argument('-m', '--max', type=int, metavar='N', 
	help='Number to stop at. (N>=1)', required=True)

parser.add_argument('-o', '--out', help='Output filename', required=True)

args = parser.parse_args()

##########
## Globals
nodes = []

##########
## Return next number in Collatz sequence

def collatz_draw(n):
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
	print('Working on %s...' % n)
	collatz_draw(n)

# Draw
graph.render(args.out)