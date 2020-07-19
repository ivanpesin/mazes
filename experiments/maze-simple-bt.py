#!/usr/bin/env python3

''' 
Very simple implementation of maze generation, solving, and ascii visualization 
Inspired: http://weblog.jamisbuck.org/2011/2/1/maze-generation-binary-tree-algorithm.html
'''

import sys
import time
import random
import argparse

# constants for maze navigation
NORTH = 1 << 0
SOUTH = 1 << 1
EAST  = 1 << 2
WEST  = 1 << 3

DX = { NORTH: 0, SOUTH: 0, EAST: 1, WEST: -1 }
DY = { NORTH: -1, SOUTH: 1, EAST: 0, WEST: 0 }
REVERSE = { NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST }

def build_maze():
    for r in range(N):
        for c in range(N):
            sides = []
            if r > 0: sides.append(NORTH)
            if c > 0: sides.append(WEST)

            if sides:
                # pick heading
                heading = random.choice(sides)

                # cell coords of where are we heading
                nr, nc = r + DY[heading], c + DX[heading] 

                # remove the wall in current and adj cells
                maze[r][c] &= ~heading
                maze[nr][nc] &= ~REVERSE[heading]

                # update the maze
                draw_maze()
                time.sleep(0.02)

def draw_maze():

    print("\033[H",end='')
    print(" %s" % ('_' * (2*N-1)))
    for r in range(N):
        print("|",end='')
        for c in range(N):
            if r == N-1: print("_",end='')
            else:
                if maze[r][c] & SOUTH: print("_",end='')
                else: print(" ",end='')

            if c < N-1: 
                if maze[r][c] & EAST: print("|",end='')
                else: 
                    # if two adj cells don't have a vertical wall
                    # and both have SOUTH walls, draw "_" to make 
                    # the horizontal wall look contiguous
                    if ((maze[r][c]   & SOUTH) and
                        (maze[r][c+1] & SOUTH)):
                         print("_",end='')
                    else: print(" ",end='')

            sys.stdout.flush()

        print("|")

# --- main:
parser = argparse.ArgumentParser(description='Creates and solved an NxN maze using binary tree algorithm.')
parser.add_argument('-n', default=10, type=int, help='maze size')
parser.add_argument('-s', default=None, type=int, help='PRG seed')
args = parser.parse_args()

# init random generator
random.seed(args.s)

# maze size
N = args.n

# init fully walled maze
maze = [ [ NORTH | SOUTH | EAST | WEST ] * N for _ in range(N) ]

# cls
print("\033[H\033[2J",end='')

build_maze()
draw_maze()