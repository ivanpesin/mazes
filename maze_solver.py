
import maze as mz
import random

class dfs:

    def __init__(self, maze, visualizer, start_row, start_col, end_row, end_col):
        self.maze       = maze
        self.visualizer = visualizer
        self.start_row  = start_row
        self.start_col  = start_col
        self.end_row    = end_row
        self.end_col    = end_col

        self.solved = False
        self.visited = [ [False] * maze.N for _ in range(maze.N) ]

        self.maze.add_tile_state(start_row, start_col, mz.ST_START)
        self.maze.add_tile_state(end_row, end_col, mz.ST_END)
        # updating the end position; start position will be updated 
        # by solver when it starts waling
        self.visualizer.update_tk_maze(end_row, end_col) 

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
        self.visualizer.update_tk_maze(r,c,redraw=True)
        self.visualizer.sleep(div=2)
        self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
        self.visualizer.update_tk_maze(r,c)

        if (r,c) == (self.end_row, self.end_col):
            self.solved = True
            return

        nbrs = self.connected_nbrs(r,c)
        random.shuffle(nbrs)

        while len(nbrs) > 0:
            nr, nc = nbrs.pop()
            if not self.visited[nr][nc]:
                self.maze_solver(nr, nc)

                if not self.solved: # don't backtrack the correct path
                    self.maze.add_tile_state(r,c,mz.ST_CURRENT | mz.ST_CORRECT_PATH)
                    self.visualizer.update_tk_maze(r,c,redraw=True)
                    self.visualizer.sleep(div=2)
                    self.maze.clear_tile_state(r,c,mz.ST_CURRENT)
                    self.visualizer.update_tk_maze(r,c)

        if not self.solved: # don't backtrack the correct path
            self.maze.set_tile_state(r,c,mz.ST_DEADEND)
            self.visualizer.update_tk_maze(r,c)