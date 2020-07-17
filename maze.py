

N, S, E, W = 1, 2, 4, 8
ST_CURRENT, ST_VISITED, ST_PATH, ST_DEADEND = 1,2,4,8
ST_CORRECT_PATH, ST_START, ST_END = 16, 32, 64

class Maze:

    def __init__(self, N=10, walls=True):
        self.N = N

        self.north = [ [walls] * N for _ in range(N) ]
        self.south = [ [walls] * N for _ in range(N) ]
        self.east  = [ [walls] * N for _ in range(N) ]
        self.west  = [ [walls] * N for _ in range(N) ]

        self.state = [ [0] * N for _ in range(N) ]

    def wall_bilder(self, r,c,direction,present):

        if direction == N:
            self.north[r][c] = present
            if r > 0: 
                self.south[r-1][c] = present
        elif direction == S:
            self.south[r][c] = present
            if r+1 < self.N: 
                self.north[r+1][c] = present
        elif direction == E:
            self.east[r][c] = present
            if c+1 < self.N:
                self.west[r][c+1] = present
        else:
            self.west[r][c]   = present
            if c > 0:
                self.east[r][c-1] = present

    def add_wall(self, r,c,d):
        self.wall_bilder(r,c,d,True)

    def remove_wall(self, r,c,d):
        self.wall_bilder(r,c,d,False)

    def has_wall(self, r,c,d):
        if d == N: return self.north[r][c]
        if d == S: return self.south[r][c]  
        if d == E: return self.east[r][c]  
        if d == W: return self.west[r][c]  

    def set_tile_state(self, r,c, state):
        self.state[r][c] = state

    def add_tile_state(self, r,c, state):
        self.state[r][c] |= state

    def clear_tile_state(self, r,c, state):
        self.state[r][c] &= ~state

    def tile_state(self, r,c):
        return self.state[r][c]
