#!/usr/bin/env python3

import maze
import maze_generator
import maze_solver
import maze_visualizer
import tkinter
import time
import argparse
import random
import sys

ALGS_LIST = [
    'Recursive split 50/50',
    'Recursive split at random',
    'Recursive backtracking'
]

def show_algs():
    ''' Lists supported maze generation algorithms '''
    print("List of supported maze generation algorithms:\n")
    for i, name in enumerate(ALGS_LIST):
        print("\t%d\t%s" % (i, name))

    
# init random generator
random.seed()
sys.setrecursionlimit(10**6) 

# parse the command line
parser = argparse.ArgumentParser(description='Creates an NxN maze using the specified algorithm.')
parser.add_argument('-a', default=0, type=int,   help="maze generation algorithm")
parser.add_argument('--algs', action="store_true", help="list supported maze generation algorithms")
parser.add_argument('-d', default=0, type=float, help="simulation delay in seconds, can be a fraction")
parser.add_argument('-n', default=10, type=int,  help="maze dimention")
parser.add_argument('-w', default=10, type=int,  help="tile width")
parser.add_argument('--start', nargs=2, type=int, default=[0,0], help="maze entrance coordinates")
parser.add_argument('--finish', nargs=2, type=int, help="maze exit coordinates")
args = parser.parse_args()

# show supported algorithms and exit
if args.algs:
    show_algs()
    sys.exit()

# check start/finish coordinates are valid
x, y = args.start
if x < 0 or x >= args.n or y < 0 or y >= args.n:
    print('Error: starting position [%d,%d] is out of maze [0..%d]' % (x,y,args.n-1), file=sys.stderr)
    sys.exit(1)

if args.finish is None: args.finish = [ args.n-1, args.n-1 ]
x, y = args.finish

if x < 0 or x >= args.n or y < 0 or y >= args.n:
    print('Error: finishing position [%d,%d] is out of maze [0..%d]' % (x,y,args.n-1), file=sys.stderr)
    sys.exit(1)


# create tkinter root
tk = tkinter.Tk()
tk.title('Maze')
tk.geometry('+100+100')

# create a maze; algs 0-4 start with empty maze and build walls, 
# others carve doors in a maze full of walls
if args.a in [0,1]: m = maze.Maze(N=args.n, walls=False)
else: m = maze.Maze(N=args.n)

# create visualizator to use with generation and solving of the maze
vis = maze_visualizer.MazeVisualizer(m, tk, tile_width=args.w, delay=args.d)
vis.draw_tk_maze()
time.sleep(3)

# ---
if   args.a == 0: 
    vis.set_statusbar('Generating the maze: recursive half-split')
    maze_generator.RecursiveSplit(m,vis)
elif args.a == 1: 
    vis.set_statusbar('Generating the maze: recursive random split')
    maze_generator.RecursiveSplit(m,vis,mode='random')
elif args.a == 2: 
    vis.set_statusbar('Generating the maze: recursive backtracking')
    maze_generator.RecursiveBacktracking(m,vis)

vis.set_statusbar('Generated, sleeping 3 sec...')
time.sleep(3)

vis.set_statusbar('Solving the maze...')
maze_solver.dfs(m,vis,*args.start,*args.finish)

vis.set_statusbar('Solved, close the window to exit.')
tk.mainloop()