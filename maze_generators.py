import maze as mz
import maze_visualizer as mv
import random
import UF

def nbrs_list(size,r,c):
    ''' return a list of neighbour cells in the maze '''
    nbrs = []

    if r-1 >= 0:   nbrs.append((r-1,c))
    if r+1 < size: nbrs.append((r+1,c))
    if c-1 >= 0:   nbrs.append((r,c-1))
    if c+1 < size: nbrs.append((r,c+1))

    return nbrs

def heading(r,c,nr,nc):
    ''' returns heading given two pairs of coords in a maze '''
    if nr-r == 1:    return mz.SOUTH
    elif nr-r == -1: return mz.NORTH
    elif nc-c == 1:  return mz.EAST
    else:            return mz.WEST

def to_cell(r,c,h):
    ''' returns cell coords given starting coords and heading '''
    if h == mz.NORTH: return (r-1,c)
    if h == mz.SOUTH: return (r+1,c)
    if h == mz.EAST:  return (r,c+1)
    if h == mz.WEST:  return (r,c-1)

class RecursiveSplit:

    def __init__(self, maze, visualizer, animate=False, mode='halves'):
        self.maze = maze
        self.visualizer = visualizer
        self.mode = mode
        self.animate = animate

        if mode in ('',None): mode = 'halves'
        if mode not in ('h','halves','r','random'):
            raise Exception('Invalid algorithm configuration, see alg description parameters')

        self.split(0,0,maze.N-1,maze.N-1,True)

    def split(self,r1,c1,r2,c2,vertical):
        ''' 
        Build a maze using recursive splitting alg
        '''

        if r1 == r2 or c1 == c2: return

        if vertical:
            # pick a column to split at
            if self.mode in ('h','halves'): pos = c1+(c2-c1)//2
            else: pos = c1 + random.randrange(c2-c1)

            for r in range(r1,r2+1):
                self.maze.add_wall(r,pos,mz.EAST)
                self.visualizer.update_tk_maze(r,pos)

            if self.animate: self.visualizer.redraw_tk_maze()

            # pick a door at random
            door = random.randrange(r1,r2+1)
            self.maze.remove_wall(door,pos,mz.EAST)
            self.visualizer.update_tk_maze(door,pos,redraw=self.animate)
            
            # recursively split two new parts
            self.split(r1,c1,r2,pos,not vertical)
            self.split(r1,pos+1,r2,c2,not vertical)

        else:
            # pick a raw to split at
            if self.mode in ('h','halves'): pos = r1 + (r2-r1)//2
            else: pos = r1 + random.randrange(r2-r1)

            for c in range(c1,c2+1):
                self.maze.add_wall(pos,c,mz.SOUTH)
                self.visualizer.update_tk_maze(pos,c)

            if self.animate: self.visualizer.redraw_tk_maze()

            # pick a door at random
            door = random.randrange(c1,c2+1)
            self.maze.remove_wall(pos,door,mz.SOUTH)
            self.visualizer.update_tk_maze(pos,door,redraw=self.animate)

            # recursively split two new parts
            self.split(r1,c1,pos,c2,not vertical)
            self.split(pos+1,c1,r2,c2,not vertical)

class RecursiveBacktracking:

    def __init__(self, maze, visualizer, animate=False):
        self.maze = maze
        self.visualizer = visualizer
        self.animate = animate

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.carve(0,0)

    def carve(self,r,c):
        ''' Build a maze using recursive backtracking alg '''

        self.visited[r][c] = True

        self.visualizer.add_tile_state(r,c,mv.ST_CURRENT | mv.ST_PATH,redraw=self.animate)
        self.visualizer.clear_tile_state(r,c,mv.ST_CURRENT)

        nbrs = nbrs_list(self.maze.N, r,c)
        random.shuffle(nbrs)

        while nbrs:
            nr, nc = nbrs.pop()
            if self.visited[nr][nc]: continue

            # remove wall
            self.maze.remove_wall(r,c,heading(r,c,nr,nc))

            # recurse into new cell
            self.carve(nr, nc)

            self.visualizer.add_tile_state(r,c,mv.ST_CURRENT | mv.ST_PATH,redraw=self.animate)             
            self.visualizer.clear_tile_state(r,c,mv.ST_CURRENT)

        # backtrack
        self.visualizer.set_tile_state(r,c,mv.ST_VISITED)

class HuntAndKill:

    def __init__(self, maze, visualizer, animate=False):
        self.maze = maze
        self.visualizer = visualizer
        self.animate = animate
        self.scan_line_start = 0

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.process(0,0)

    def process(self, r,c):
        ''' Loop through walking and hunting while not done '''
        done = False
        while not done:
            r,c, deadend = self.walk(r,c)
            if deadend: r,c, done = self.hunt()

    def walk(self, r,c):
        ''' walk to next unvisited cell '''
        
        self.visited[r][c] = True

        self.visualizer.add_tile_state(r,c,mv.ST_CURRENT | mv.ST_VISITED,redraw=self.animate)
        self.visualizer.clear_tile_state(r,c,mv.ST_CURRENT)

        nbrs = nbrs_list(self.maze.N, r,c)
        random.shuffle(nbrs)

        while nbrs:
            nr, nc = nbrs.pop()
            if self.visited[nr][nc]: continue

            # carve wall and return
            self.maze.remove_wall(r,c,heading(r,c,nr,nc))
    
            return nr,nc,False

        # deadend
        return r,c,True

    def vis_scan_line(self, r):
        ''' highlights the scanning row in visualizer '''

        # set tile state
        for c in range(self.maze.N):
            self.visualizer.add_tile_state(r,c,mv.ST_CORRECT_PATH)
        
        if self.animate: self.visualizer.redraw_tk_maze()
        
        # clear tile state
        for c in range(self.maze.N):
            self.visualizer.clear_tile_state(r,c,mv.ST_CORRECT_PATH)

    def hunt(self):
        ''' 
        find an unvisited cell adjacent to a visited one;
        remove the wall between two and use unvisited cell 
        as a starting lcation for a walk
        '''
        for r in range(self.scan_line_start,self.maze.N):
            self.vis_scan_line(r)
            for c in range(self.maze.N):
                if not self.visited[r][c]:
                    nbrs = nbrs_list(self.maze.N, r,c)
                    random.shuffle(nbrs)

                    while nbrs:
                        nr, nc = nbrs.pop()
                        if not self.visited[nr][nc]: continue

                        # carve wall and return
                        self.maze.remove_wall(r,c, heading(r,c,nr,nc))

                        return r,c,False

            # this row has no unvisited cells, so
            # skip re-scanning it
            self.scan_line_start += 1

        # no unvisited tiles
        return 0,0,True

class BinaryTree:

    def __init__(self, maze, visualizer, mode='SE', animate=False):
        self.maze = maze
        self.visualizer = visualizer
        self.animate = animate
        self.mode = mode.upper() if mode is not None else 'SE'

        if self.mode not in ('NW','NE','SW','SE'):
            raise Exception('Invalid algorithm configuration, see alg description parameters')

        self.generate(0,0)

    def generate(self, r,c):
        ''' Generates a maze '''

        for r in range(self.maze.N):
            for c in range(self.maze.N):
                
                headings = []
                if self.mode == 'NW':
                    if r > 0:             headings.append(mz.NORTH)      
                    if c > 0:             headings.append(mz.WEST)
                elif self.mode == 'NE':
                    if r > 0:             headings.append(mz.NORTH)      
                    if c < self.maze.N-1: headings.append(mz.EAST)
                elif self.mode == 'SW':
                    if r < self.maze.N-1: headings.append(mz.SOUTH)                
                    if c > 0:             headings.append(mz.WEST)
                else: # 'SE'
                    if r < self.maze.N-1: headings.append(mz.SOUTH)                
                    if c < self.maze.N-1: headings.append(mz.EAST)
                random.shuffle(headings)

                if headings:
                    h = headings.pop()
                    self.maze.remove_wall(r,c,h)
                
                self.visualizer.add_tile_state(r,c,mv.ST_VISITED | mv.ST_CURRENT, redraw=self.animate)
                self.visualizer.clear_tile_state(r,c,mv.ST_CURRENT)
                
class GrowingTree:
    '''
    Growing tree algorithm

    1. Let C be a list of cells, initially empty. Add one cell to C, at random.
    2. Choose a cell from C, and carve a passage to any unvisited neighbor of 
       that cell, adding that neighbor to C as well. 
       If there are no unvisited neighbors, remove the cell from C.
    3. Repeat #2 until C is empty.
    '''

    def __init__(self, maze, visualizer, animate=False, mode='r'):
        self.maze = maze
        self.visualizer = visualizer
        self.mode = mode
        self.animate = animate

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        # start at a random position
        r, c = random.randrange(maze.N),random.randrange(maze.N)
        self.frontier = [ (r,c) ]
        self.visited[r][c] = True

        self.visualizer.set_tile_state(r,c, mv.ST_PATH | mv.ST_VISITED, redraw=self.animate)
        
        self.grow()

    def pick_cell(self):
        ''' picks a cell according to specified mode '''
        if self.mode in ['r','random']: return random.choice(self.frontier)
        if self.mode in ['n','new','newest']: return self.frontier[-1]
        if self.mode in ['o','old','oldest']: return self.frontier[0]
        if self.mode in ['m','mid','middle']: return self.frontier[len(self.frontier)//2]

    def grow(self):

        while self.frontier:
            r, c = self.pick_cell()

            # get unvisited neighbours
            nbrs = [ (nr,nc) for nr,nc in nbrs_list(self.maze.N,r,c) if not self.visited[nr][nc] ]

            if not nbrs:
                self.frontier.remove((r,c))

                self.visualizer.clear_tile_state(r,c, mv.ST_PATH, redraw=self.animate)
                continue

            nr, nc = random.choice(nbrs)
            self.maze.remove_wall(r,c,heading(r,c,nr,nc))
            self.visited[nr][nc] = True
            
            self.visualizer.set_tile_state(nr,nc, mv.ST_PATH | mv.ST_VISITED, redraw=self.animate)

            if (nr,nc) not in self.frontier:
                self.frontier.append((nr,nc))


class Kruskals:
    '''
    1. Put all edges into a bag
    2. Pull out the edge with the lowest weight (or randomly for maze generation)
    3. If the edge connects two disjoint trees, join the trees. Otherwise, 
       throw that edge away.
    4. Repeat until there are no more edges left.
    '''

    def __init__(self, maze, visualizer, animate=False):
        self.maze = maze
        self.visualizer = visualizer
        self.animate = animate

        self.edges = []
        self.UF = UF.UF(maze.N ** 2)
        for r in range(maze.N):
            for c in range(maze.N):
                if c < maze.N-1: self.edges.append((r,c,mz.EAST))
                if r < maze.N-1: self.edges.append((r,c,mz.SOUTH))

        random.shuffle(self.edges)
        self.process()

    def eid(self,r,c):
        ''' calculate element id for UF '''
        return r*self.maze.N + c

    def process(self):
        cnt = 0

        while self.edges:
            r, c, h = self.edges.pop()
            nr, nc = to_cell(r,c,h)

            if self.UF.connected(self.eid(r,c),self.eid(nr,nc)): continue

            self.visualizer.set_tile_state(r,c,mv.ST_VISITED)
            self.UF.union(self.eid(r,c),self.eid(nr,nc))
            self.maze.remove_wall(r,c, heading(r,c,nr,nc))

            # redraw only every third update
            cnt += 1
            redraw = True if cnt % 3 == 0 and self.animate else False
            self.visualizer.set_tile_state(nr,nc,mv.ST_VISITED,redraw=redraw)

