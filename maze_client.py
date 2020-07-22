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
    { 'name': 'Recursive split', 'param': [ 'halves', 'random' ], 'walls': False },
    { 'name': 'Recursive backtracking', 'param':  None, 'walls': True },
    { 'name': 'Hunt-and-kill',   'param':  None, 'walls': True },
    { 'name': "Kruskal's",       'param':  None, 'walls': True },
    { 'name': 'Binary tree',     'param': [ 'NE','NW','SE','SW'], 'walls': True },
    { 'name': 'Growing tree',    'param': [ '<policy:weight>[,<policy:weight>...]'], 'walls': True }
]

def show_algs():
    ''' Lists supported maze generation algorithms '''
    print("List of supported maze generation algorithms:\n")
    for i, desc in enumerate(ALGS_LIST):
        print("\t%d\t%s" % (i, desc['name']))
        if desc['param']: print("\t\tParameters: %s" % (desc['param'])) 

    footer = '''
All parameters are optional, algorithms use built-in defaults.
    
Growing tree algorithm supports following policies:

    o|oldest,n|newest,r|random,m|middle

Default policy is "r" which always select the oldest element from stack
which effectively implements Prim's algorithm. Other interesting combinations:

    n       Always select newest element from stack, 
            implements Recursive Backtracking
    
'''
    print(footer)
    
    
# --- main

# parse the command line
parser = argparse.ArgumentParser(
    description='Creates an NxN maze using the specified algorithm.',
    epilog='Rows and columns indices start with 0 in the top-right corner.')
parser_gen = parser.add_argument_group('maze generation')
parser_gen.add_argument('-n',            default=10, type=int,  help="maze size")
parser_gen.add_argument('-a',            default=0, type=int,   help="maze generation algorithm")
parser_gen.add_argument('--algs',        action="store_true",   help="list supported maze generation algorithms")
parser_gen.add_argument('-p',            type=str,  help="algorithm parameters, see alg list for details")
parser_gen.add_argument('-s',            default=None, type=int,help="random seed, use to generate repeatable mazes")

parser_vis = parser.add_argument_group('maze visualization')
parser_vis.add_argument('-d',            default=0, type=float, help="simulation delay in seconds, can be a fraction")
parser_vis.add_argument('--start_delay', default=2, type=int,   help="start delay in seconds, can be a fraction")
parser_vis.add_argument('--animate',     default='both', choices=['no','gen','sol','both'], help="algorithms animation")
parser_vis.add_argument('-w',            default=10, type=int,  help="tile width in px")

parser_sol = parser.add_argument_group('maze solving')
parser_sol.add_argument('--start',       nargs=2, type=int,     help="maze entrance coordinates", default=[0,0], metavar=('row', 'col'))
parser_sol.add_argument('--finish',      nargs=2, type=int,     help="maze exit coordinates", metavar=('row', 'col'))
parser_sol.add_argument('--solver', default='dfs', choices=['dfs','bfs'], help="maze solver algorithm")
args = parser.parse_args()

# show supported algorithms and exit
if args.algs or args.a not in range(len(ALGS_LIST)):
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
m = maze.Maze(N=args.n, walls=ALGS_LIST[args.a]['walls'])

# create visualizator to use with generation and solving of the maze
vis = maze_visualizer.MazeVisualizer(m, tk, tile_width=args.w, delay=args.d)
vis.draw_maze()
vis.set_statusbar('Start delay: %d sec ...' % args.start_delay)
time.sleep(args.start_delay)

# generating
mode = None
desc = ALGS_LIST[args.a]['name']
if args.p:
    mode = args.p
    desc += " (%s)" % args.p
vis.set_statusbar('Generating the maze: %s' % ALGS_LIST[args.a]['name'])

animate = True if args.animate in [ 'gen','both' ] else False

try:
    if   args.a == 0: maze_generators.RecursiveSplit(m,vis,animate=animate,mode=mode)
    elif args.a == 1: maze_generators.RecursiveBacktracking(m,vis,animate=animate)
    elif args.a == 2: maze_generators.HuntAndKill(m,vis,animate=animate)
    elif args.a == 3: maze_generators.Kruskals(m,vis,animate=animate)
    elif args.a == 4: maze_generators.BinaryTree(m,vis,mode=mode,animate=animate)
    elif args.a == 5: maze_generators.GrowingTree(m,vis,mode=mode,animate=animate)
except Exception as err:
    print(err)
    sys.exit(2)



vis.set_statusbar('Generated, sleeping 3 sec...')
time.sleep(3)

# solving
vis.set_statusbar('Solving the maze using %s' % args.solver)

animate = True if args.animate in [ 'sol','both' ] else False

if args.solver == 'dfs': maze_solver.dfs(m,vis,*args.start,*args.finish,animate=animate)
else: maze_solver.bfs(m,vis,*args.start,*args.finish,animate=animate)

vis.set_statusbar('Solved, close the window to exit.')
tk.mainloop()