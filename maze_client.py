#!/usr/bin/env python3

import maze
import maze_generators
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
    'Recursive backtracking',
    'Hunt-and-kill',
    'Binary tree (SE biased)',
    "Growing tree (Prim's)",
]

def show_algs():
    ''' Lists supported maze generation algorithms '''
    print("List of supported maze generation algorithms:\n")
    for i, name in enumerate(ALGS_LIST):
        print("\t%d\t%s" % (i, name))

    
# --- main

# parse the command line
parser = argparse.ArgumentParser(description='Creates an NxN maze using the specified algorithm.')
parser.add_argument('-a',            default=0, type=int,   help="maze generation algorithm")
parser.add_argument('--algs',        action="store_true",   help="list supported maze generation algorithms")
parser.add_argument('-d',            default=0, type=float, help="simulation delay in seconds, can be a fraction")
parser.add_argument('--start_delay', default=2, type=int,   help="delay on start, can be a fraction")
parser.add_argument('-n',            default=10, type=int,  help="maze size")
parser.add_argument('-s',            default=None, type=int,help="random seed")
parser.add_argument('-w',            default=10, type=int,  help="tile width")
parser.add_argument('--start', nargs=2, type=int, default=[0,0], help="maze entrance coordinates")
parser.add_argument('--finish', nargs=2, type=int,          help="maze exit coordinates")
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

# init random generator
random.seed(args.s)
sys.setrecursionlimit(10**6) 

# create tkinter root
tk = tkinter.Tk()
tk.title('Maze')
tk.geometry('+100+100')
tk.lift()

# create a maze; some algs start with an empty maze and build walls, 
# others carve doors in a maze full of walls
if args.a in [0,1]: m = maze.Maze(N=args.n, walls=False)
else: m = maze.Maze(N=args.n)

# create visualizator to use with generation and solving of the maze
vis = maze_visualizer.MazeVisualizer(m, tk, tile_width=args.w, delay=args.d)
vis.draw_maze()
vis.set_statusbar('Start delay: %d sec ...' % args.start_delay)
time.sleep(args.start_delay)

# ---
vis.set_statusbar('Generating the maze: %s' % ALGS_LIST[args.a])

if   args.a == 0: maze_generators.RecursiveSplit(m,vis)
elif args.a == 1: maze_generators.RecursiveSplit(m,vis,mode='random')
elif args.a == 2: maze_generators.RecursiveBacktracking(m,vis)
elif args.a == 3: maze_generators.HuntAndKill(m,vis)
elif args.a == 4: maze_generators.BinaryTree(m,vis)
elif args.a == 5: maze_generators.GrowingTree(m,vis)


vis.set_statusbar('Generated, sleeping 3 sec...')
time.sleep(3)

vis.set_statusbar('Solving the maze...')
maze_solver.dfs(m,vis,*args.start,*args.finish)

vis.set_statusbar('Solved, close the window to exit.')
tk.mainloop()