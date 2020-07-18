import maze as mz
import random

class RecursiveSplit:

    def __init__(self, maze, visualizer, mode='halves'):
        self.maze = maze
        self.visualizer = visualizer
        self.mode = mode

        self.split(0,0,maze.N-1,maze.N-1,True)

    def split(self,r1,c1,r2,c2,vertical):
        ''' 
        Build a maze using recursive splitting alg
        Always splits 50/50 and reverses wall direction at each step
        '''
        if r1 == r2 or c1 == c2: return

        if vertical:
            if self.mode == 'halves': pos = c1+(c2-c1)//2
            else:
                pos = c1 + random.randrange(c2-c1)

            for r in range(r1,r2+1):
                self.maze.add_wall(r,pos,mz.E)

            self.visualizer.draw_tk_maze()
            self.visualizer.sleep(div=2)

            # pick a door at random
            door = random.randrange(r1,r2+1)
            self.maze.remove_wall(door,pos,mz.E)
            self.visualizer.draw_tk_maze()
            self.visualizer.sleep(div=2)
            
            # recursively split two new parts
            self.split(r1,c1,r2,pos,not vertical)
            self.split(r1,pos+1,r2,c2,not vertical)

        else:
            if self.mode == 'halves': pos = r1 + (r2-r1)//2
            else:
                pos = r1 + random.randrange(r2-r1)

            for c in range(c1,c2+1):
                self.maze.add_wall(pos,c,mz.S)

            self.visualizer.draw_tk_maze()
            self.visualizer.sleep(div=2)

            # pick a door at random
            door = random.randrange(c1,c2+1)
            self.maze.remove_wall(pos,door,mz.S)
            self.visualizer.draw_tk_maze()
            self.visualizer.sleep(div=2)

            # recursively split two new parts
            self.split(r1,c1,pos,c2,not vertical)
            self.split(pos+1,c1,r2,c2,not vertical)

class RecursiveBacktracking:

    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.carve(0,0)

    def all_nbrs(self, r,c):
        ''' return a list of neighbour cells in the maze '''
        nbrs = []

        if r-1 >= 0:          nbrs.append((r-1,c))
        if r+1 < self.maze.N: nbrs.append((r+1,c))
        if c-1 >= 0:          nbrs.append((r,c-1))
        if c+1 < self.maze.N: nbrs.append((r,c+1))

        return nbrs

    def carve(self,r,c):
        ''' Build a maze using recursive backtracking alg '''

        self.visited[r][c] = True

        self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_PATH)
        self.visualizer.update_tk_maze(r,c,redraw=True)
        self.visualizer.sleep(div=2)
        self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
        self.visualizer.update_tk_maze(r,c)

        nbrs = self.all_nbrs(r,c)
        random.shuffle(nbrs)

        while len(nbrs) > 0:
            nr, nc = nbrs.pop()
            if self.visited[nr][nc]: continue
            if nr-r == 1:
                self.maze.remove_wall(r,c,mz.S)
                self.maze.remove_wall(nr,nc,mz.N)
            elif nr-r == -1:
                self.maze.remove_wall(r,c,mz.N)
                self.maze.remove_wall(nr,nc,mz.S)
            elif nc-c == 1:
                self.maze.remove_wall(r,c,mz.E)
                self.maze.remove_wall(nr,nc,mz.W)
            else:
                self.maze.remove_wall(r,c,mz.W)
                self.maze.remove_wall(nr,nc,mz.E)

            self.carve(nr, nc)

            self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_PATH)
            self.visualizer.update_tk_maze(r,c,redraw=True)
            self.visualizer.sleep(div=2)                
            self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
            self.visualizer.update_tk_maze(r,c)

        self.maze.set_tile_state(r,c,mz.ST_VISITED)
        self.visualizer.update_tk_maze(r,c)

class HuntAndKill:

    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.scan_line_start = 0

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.process(0,0)

    def all_nbrs(self, r,c):
        ''' return a list of neighbour cells in the maze '''
        nbrs = []

        if r-1 >= 0:          nbrs.append((r-1,c))
        if r+1 < self.maze.N: nbrs.append((r+1,c))
        if c-1 >= 0:          nbrs.append((r,c-1))
        if c+1 < self.maze.N: nbrs.append((r,c+1))

        return nbrs

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
        self.visualizer.sleep(div=2)
        self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
        self.visualizer.update_tk_maze(r,c)

        nbrs = self.all_nbrs(r,c)
        random.shuffle(nbrs)

        while len(nbrs) > 0:
            nr, nc = nbrs.pop()
            if self.visited[nr][nc]: continue
            if nr-r == 1:
                self.maze.remove_wall(r,c,mz.S)
                self.maze.remove_wall(nr,nc,mz.N)
            elif nr-r == -1:
                self.maze.remove_wall(r,c,mz.N)
                self.maze.remove_wall(nr,nc,mz.S)
            elif nc-c == 1:
                self.maze.remove_wall(r,c,mz.E)
                self.maze.remove_wall(nr,nc,mz.W)
            else:
                self.maze.remove_wall(r,c,mz.W)
                self.maze.remove_wall(nr,nc,mz.E)
    
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
        self.visualizer.sleep(div=2)

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
                    nbrs = self.all_nbrs(r,c)
                    random.shuffle(nbrs)

                    while len(nbrs) > 0:
                        nr, nc = nbrs.pop()
                        if not self.visited[nr][nc]: continue
                        # carve wall and return
                        if nr-r == 1:
                            self.maze.remove_wall(r,c,mz.S)
                            self.maze.remove_wall(nr,nc,mz.N)
                        elif nr-r == -1:
                            self.maze.remove_wall(r,c,mz.N)
                            self.maze.remove_wall(nr,nc,mz.S)
                        elif nc-c == 1:
                            self.maze.remove_wall(r,c,mz.E)
                            self.maze.remove_wall(nr,nc,mz.W)
                        else:
                            self.maze.remove_wall(r,c,mz.W)
                            self.maze.remove_wall(nr,nc,mz.E)                        
                        return r,c,False

            # this row has no unvisited cells, so
            # skip re-scanning it
            self.scan_line_start += 1

        # no unvisited tiles
        return 0,0,True





