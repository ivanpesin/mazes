import maze as mz
import random

def nbrs_list(size,r,c):
    ''' return a list of neighbour cells in the maze '''
    nbrs = []

    if r-1 >= 0:   nbrs.append((r-1,c))
    if r+1 < size: nbrs.append((r+1,c))
    if c-1 >= 0:   nbrs.append((r,c-1))
    if c+1 < size: nbrs.append((r,c+1))

    return nbrs

def heading(r,c,nr,nc):
    
    if nr-r == 1:    return mz.S
    elif nr-r == -1: return mz.N
    elif nc-c == 1:  return mz.E
    else:            return mz.W

class RecursiveSplit:

    def __init__(self, maze, visualizer, animate=False, mode='halves'):
        self.maze = maze
        self.visualizer = visualizer
        self.mode = mode
        self.animate = animate

        self.split(0,0,maze.N-1,maze.N-1,True)

    def split(self,r1,c1,r2,c2,vertical):
        ''' 
        Build a maze using recursive splitting alg
        '''

        if r1 == r2 or c1 == c2: return

        if vertical:
            # pick a column to split at
            if self.mode == 'halves': pos = c1+(c2-c1)//2
            else: pos = c1 + random.randrange(c2-c1)

            for r in range(r1,r2+1):
                self.maze.add_wall(r,pos,mz.E)
                self.visualizer.update_tk_maze(r,pos)

            # redraw the maze
            self.visualizer.update_tk_maze(r1,c1,redraw=self.animate)

            # pick a door at random
            door = random.randrange(r1,r2+1)
            self.maze.remove_wall(door,pos,mz.E)
            self.visualizer.update_tk_maze(door,pos,redraw=self.animate)
            
            # recursively split two new parts
            self.split(r1,c1,r2,pos,not vertical)
            self.split(r1,pos+1,r2,c2,not vertical)

        else:
            # pick a raw to split at
            if self.mode == 'halves': pos = r1 + (r2-r1)//2
            else: pos = r1 + random.randrange(r2-r1)

            for c in range(c1,c2+1):
                self.maze.add_wall(pos,c,mz.S)
                self.visualizer.update_tk_maze(pos,c)

            # redraw the maze
            self.visualizer.update_tk_maze(r1,c1,redraw=self.animate)

            # pick a door at random
            door = random.randrange(c1,c2+1)
            self.maze.remove_wall(pos,door,mz.S)
            self.visualizer.update_tk_maze(pos,door,redraw=self.animate)

            # recursively split two new parts
            self.split(r1,c1,pos,c2,not vertical)
            self.split(pos+1,c1,r2,c2,not vertical)

class RecursiveBacktracking:

    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.carve(0,0)

    def carve(self,r,c):
        ''' Build a maze using recursive backtracking alg '''

        self.visited[r][c] = True

        self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_PATH)
        self.visualizer.update_tk_maze(r,c,redraw=True)
        self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
        self.visualizer.update_tk_maze(r,c)

        nbrs = nbrs_list(self.maze.N, r,c)
        random.shuffle(nbrs)

        while nbrs:
            nr, nc = nbrs.pop()
            if self.visited[nr][nc]: continue

            if nr-r == 1:    self.maze.remove_wall(r,c,mz.S)
            elif nr-r == -1: self.maze.remove_wall(r,c,mz.N)
            elif nc-c == 1:  self.maze.remove_wall(r,c,mz.E)
            else:            self.maze.remove_wall(r,c,mz.W)

            self.carve(nr, nc)

            self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_PATH)
            self.visualizer.update_tk_maze(r,c,redraw=True)               
            self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
            self.visualizer.update_tk_maze(r,c)

        # backtrack
        self.maze.set_tile_state(r,c,mz.ST_VISITED)
        self.visualizer.update_tk_maze(r,c)

class HuntAndKill:

    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.scan_line_start = 0

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.process(0,0)

    def process(self, r,c):
        ''' Loop through walking and hunting while not done '''
        done = False
        while not done:
            r,c,deadend = self.walk(r,c)
            if deadend: r,c,done = self.hunt()

        #self.visualizer.draw_maze()

    def walk(self, r,c):
        ''' walk to next unvisited cell '''
        
        self.visited[r][c] = True

        self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_VISITED)
        self.visualizer.update_tk_maze(r,c,redraw=True)
        self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
        self.visualizer.update_tk_maze(r,c)

        nbrs = nbrs_list(self.maze.N, r,c)
        random.shuffle(nbrs)

        while nbrs:
            nr, nc = nbrs.pop()
            if self.visited[nr][nc]: continue

            if nr-r == 1:    self.maze.remove_wall(r,c,mz.S)
            elif nr-r == -1: self.maze.remove_wall(r,c,mz.N)
            elif nc-c == 1:  self.maze.remove_wall(r,c,mz.E)
            else:            self.maze.remove_wall(r,c,mz.W)
    
            return nr,nc,False

        # deadend
        return r,c,True

    def vis_scan_line(self, r):
        ''' highlights the scanning row in visualizer '''

        # set tile state
        for c in range(self.maze.N):
            self.maze.add_tile_state(r,c,mz.ST_CORRECT_PATH)
            self.visualizer.update_tk_maze(r,c)
        # redraw
        self.visualizer.update_tk_maze(r,0,redraw=True)
        # clear tile state
        for c in range(self.maze.N):
            self.maze.clear_tile_state(r,c,mz.ST_CORRECT_PATH)
            self.visualizer.update_tk_maze(r,c)

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

    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

        self.generate(0,0)

    def generate(self, r,c):
        ''' Generates south-east biased maze '''

        for r in range(self.maze.N):
            for c in range(self.maze.N):
                
                headings = []
                if r < self.maze.N-1: headings.append(mz.S)                
                if c < self.maze.N-1: headings.append(mz.E)
                random.shuffle(headings)

                if headings > 0:
                    h = headings.pop()
                    self.maze.remove_wall(r,c,h)
                
                self.maze.add_tile_state(r,c,mz.ST_VISITED | mz.ST_CURRENT)
                self.visualizer.update_tk_maze(r,c,redraw=True)
                self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
                self.visualizer.update_tk_maze(r,c)
                
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

        self.maze.set_tile_state(r,c, mz.ST_PATH | mz.ST_VISITED)
        self.visualizer.update_tk_maze(r,c,redraw=self.animate)
        
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

                self.maze.clear_tile_state(r,c, mz.ST_PATH)
                self.visualizer.update_tk_maze(r,c,redraw=self.animate)
                continue

            nr, nc = random.choice(nbrs)
            self.maze.remove_wall(r,c,heading(r,c,nr,nc))
            self.visited[nr][nc] = True
            
            self.maze.set_tile_state(nr,nc, mz.ST_PATH | mz.ST_VISITED)
            self.visualizer.update_tk_maze(nr,nc,redraw=self.animate)

            if (nr,nc) not in self.frontier:
                self.frontier.append((nr,nc))


            

