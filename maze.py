

# cardinal directions
NORTH = 1 << 0
SOUTH = 1 << 1
EAST  = 1 << 2
WEST  = 1 << 3

class Maze:

    def __init__(self, N=10, walls=True):
        self.N = N

        self.north = [ [walls] * N for _ in range(N) ]
        self.south = [ [walls] * N for _ in range(N) ]
        self.east  = [ [walls] * N for _ in range(N) ]
        self.west  = [ [walls] * N for _ in range(N) ]

    def wall_bilder(self, r,c,side,has_wall):

        if side == NORTH:
            self.north[r][c] = has_wall
            if r > 0: self.south[r-1][c] = has_wall
        elif side == SOUTH:
            self.south[r][c] = has_wall
            if r+1 < self.N: self.north[r+1][c] = has_wall
        elif side == EAST:
            self.east[r][c] = has_wall
            if c+1 < self.N: self.west[r][c+1] = has_wall
        else:
            self.west[r][c]   = has_wall
            if c > 0: self.east[r][c-1] = has_wall

    def add_wall(self, r,c,side):
        self.wall_bilder(r,c,side,has_wall=True)

    def remove_wall(self, r,c,side):
        self.wall_bilder(r,c,side,has_wall=False)

    def has_wall(self, r,c,side):
        if side == NORTH: return self.north[r][c]
        if side == SOUTH: return self.south[r][c]  
        if side == EAST: return self.east[r][c]  
        if side == WEST: return self.west[r][c]  

