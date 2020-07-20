
import maze as mz
import random

class dfs:

    def __init__(self, maze, visualizer, start_row, start_col, end_row, end_col, animate=False):
        self.maze       = maze
        self.visualizer = visualizer
        self.start_row  = start_row
        self.start_col  = start_col
        self.end_row    = end_row
        self.end_col    = end_col
        self.animate    = animate

        self.solved = False
        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        # mark start and finish positions for the solver
        self.visualizer.mark_exits(start_row, start_col,end_row, end_col)

        self.maze_solver(start_row, start_col)

    def connected_nbrs(self,r,c):
        ''' return a list of connected nieghbour cells in the maze '''
        nbrs = []

        if r-1 >= 0          and not self.maze.has_wall(r,c,mz.N): nbrs.append((r-1,c))
        if r+1 < self.maze.N and not self.maze.has_wall(r,c,mz.S): nbrs.append((r+1,c))
        if c-1 >= 0          and not self.maze.has_wall(r,c,mz.W): nbrs.append((r,c-1))
        if c+1 < self.maze.N and not self.maze.has_wall(r,c,mz.E): nbrs.append((r,c+1))

        return nbrs

    def maze_solver(self, r,c):
        ''' Just a DFS implementation with visualizer updates '''

        if self.solved == True: return

        self.visited[r][c] = True

        self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_CORRECT_PATH)
        self.visualizer.update_tk_maze(r,c,redraw=self.animate)
        self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
        self.visualizer.update_tk_maze(r,c)

        if (r,c) == (self.end_row, self.end_col):
            self.solved = True
            return

        nbrs = self.connected_nbrs(r,c)
        random.shuffle(nbrs)

        while nbrs:
            nr, nc = nbrs.pop()
            if not self.visited[nr][nc]:
                self.maze_solver(nr, nc)

                if not self.solved: # don't backtrack the correct path
                    self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_CORRECT_PATH)
                    self.visualizer.update_tk_maze(r,c,redraw=self.animate)
                    self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
                    self.visualizer.update_tk_maze(r,c)

        if not self.solved: # don't backtrack the correct path
            self.maze.set_tile_state(r,c,mz.ST_DEADEND)
            self.visualizer.update_tk_maze(r,c)

class bfs:

    def __init__(self, maze, visualizer, start_row, start_col, end_row, end_col, animate=False):
        self.maze       = maze
        self.visualizer = visualizer
        self.start_row  = start_row
        self.start_col  = start_col
        self.end_row    = end_row
        self.end_col    = end_col
        self.animate    = animate

        self.visited = [ [False] * maze.N for _ in range(maze.N) ]
        self.path_to = [ [(-1,-1)] * maze.N for _ in range(maze.N) ]
        self.solved = False

        # mark start and finish positions for the solver
        self.visualizer.mark_exits(start_row, start_col,end_row, end_col)

        # put starting position on stack
        self.stack = [(start_row, start_col)]
        self.visited[start_row][start_col] = True

        self.maze_solver()

    def connected_nbrs(self,r,c):
        ''' return a list of connected nieghbour cells in the maze '''
        nbrs = []

        if r-1 >= 0          and not self.maze.has_wall(r,c,mz.N): nbrs.append((r-1,c))
        if r+1 < self.maze.N and not self.maze.has_wall(r,c,mz.S): nbrs.append((r+1,c))
        if c-1 >= 0          and not self.maze.has_wall(r,c,mz.W): nbrs.append((r,c-1))
        if c+1 < self.maze.N and not self.maze.has_wall(r,c,mz.E): nbrs.append((r,c+1))

        return nbrs

    def maze_solver(self):
        ''' Just a BFS implementation with visualizer updates '''

        while self.stack and not self.solved:
            r, c = self.stack.pop(0)

            if (r,c) == (self.end_row,self.end_col):
                self.solved = True
                break

            nbrs = [ (nr,nc) for nr,nc in self.connected_nbrs(r,c) if not self.visited[nr][nc] ]
            
            if not nbrs: continue
            for nr, nc in nbrs:
                self.visited[nr][nc] = True
                self.path_to[nr][nc] = (r,c)
                
                # just using DEADEND color to mark visited cells
                self.maze.set_tile_state(r,c,mz.ST_DEADEND) 
                self.visualizer.update_tk_maze(r,c,redraw=self.animate)

            self.stack.extend(nbrs)

        (r,c) = (self.end_row,self.end_col)
        while (r,c) != (self.start_row,self.start_col):
            self.maze.set_tile_state(r,c,mz.ST_CORRECT_PATH)
            self.visualizer.update_tk_maze(r,c,redraw=self.animate)
            r,c = self.path_to[r][c]

        self.maze.set_tile_state(r,c,mz.ST_CORRECT_PATH)
        self.visualizer.update_tk_maze(r,c,redraw=self.animate)
        