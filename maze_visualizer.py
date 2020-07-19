import time
import tkinter
import maze as mz

class MazeVisualizer:

    BACKGROUND_COLOR='white'
    BORDER_COLOR='navy'

    COLORS = {
        'START': 'red',
        'END': 'green'
    }

    def __init__(self, maze, tk_root, tile_width=10, wall_width=1, delay=0, ascii=False):
        self.maze = maze
        self.tk_root = tk_root
        self.tile_width = tile_width
        self.wall_width = wall_width
        self.delay = delay 

        self.draw_ascii = ascii
        self.draw_tk = False

        if tkinter is not None:
            self.draw_tk = True

            self.tiles      = []
            self.wall_south = []
            self.wall_east = []

            # all tiles width + 2 for visual borders +
            # all internal walls width
            # 2 triple wall width for exterior walls

            dimentions = (maze.N+2) * tile_width + (maze.N - 1) * wall_width + 2 * wall_width * 3
            self.canvas = tkinter.Canvas(tk_root, 
                width=dimentions, height=dimentions, 
                background=self.BACKGROUND_COLOR)
            self.canvas.pack()

            self.status = tkinter.Label(tk_root, text = 'Initializing')
            self.status.pack()

    def tile_color(self,r,c):
        if self.maze.tile_state(r,c) & mz.ST_CURRENT:
            color = 'hot pink'
        elif self.maze.tile_state(r,c) & mz.ST_START:
            color = self.COLORS['START']                           
        elif self.maze.tile_state(r,c) & mz.ST_END:
            color = self.COLORS['END']             
        elif self.maze.tile_state(r,c) & mz.ST_PATH:
            color = 'pink'
        elif self.maze.tile_state(r,c) & mz.ST_CORRECT_PATH:
            color = 'lightgreen'
        elif self.maze.tile_state(r,c) & mz.ST_VISITED:
            color = 'white'
        elif self.maze.tile_state(r,c) & mz.ST_DEADEND:
            color = 'lightgray'                    
        else:
            color = 'linen'  

        return color      

    def draw_maze(self):
        if self.draw_ascii: self.draw_ascii_maze()
        if self.draw_tk:    self.draw_tk_maze()

    def draw_ascii_maze(self):
        pass

    def draw_tk_maze(self):
        '''
        Simple TK-based maze visualization. Redraws the whole maze evey time it's called.
        Slow on mazes larger than 30x30.
        '''

        self.canvas.delete(tkinter.ALL)

        # exterior walls

        x1 = self.tile_width
        y1 = x1

        x2 = self.tile_width + \
             self.maze.N * self.tile_width + \
             (self.maze.N-1) * self.wall_width + \
             self.wall_width * 3
        y2 = x2

        self.canvas.create_line(x1,y1, x1,y2, fill=self.BORDER_COLOR,width=3*self.wall_width)
        self.canvas.create_line(x2,y1, x2,y2, fill=self.BORDER_COLOR,width=3*self.wall_width)
        self.canvas.create_line(x1,y1, x2,y1, fill=self.BORDER_COLOR,width=3*self.wall_width)
        self.canvas.create_line(x1,y2, x2,y2, fill=self.BORDER_COLOR,width=3*self.wall_width)

        # inside walls

        width = self.tile_width + self.wall_width

        for r in range(self.maze.N):
            for c in range(self.maze.N):
                if self.maze.has_wall(r,c,mz.S) and r+1 < self.maze.N:
                    self.canvas.create_line(
                        (c+1)*width,(r+2)*width, 
                        (c+2)*width,(r+2)*width,
                        fill='black')
                if self.maze.has_wall(r,c,mz.E) and c+1 < self.maze.N:
                    self.canvas.create_line(
                        (c+2)*width,(r+1)*width,
                        (c+2)*width,(r+2)*width,
                        fill='black')

                x1 = (c+1)*width
                y1 = (r+1)*width
                x2 = (c+2)*width
                y2 = (r+2)*width
                if self.maze.has_wall(r,c,mz.N): y1 += self.wall_width
                #if self.maze.has_wall(r,c,maze.S): y2 -= self.wall_width
                #if self.maze.has_wall(r,c,maze.E): x2 -= self.wall_width
                if self.maze.has_wall(r,c,mz.W): x1 += self.wall_width

                color = self.tile_color(r,c)

                self.canvas.create_rectangle(
                    x1,y1, x2,y2,
                    fill=color,
                    width=0
                )

        self.tk_root.update()

    def init_tk_maze(self):
        '''
        Initializes a maze grid with tiles and walls. Then update_tk_maze(r,c) can simply
        flip the colors to update the visualization. Trickier than draw_tk_maze() but faster.
        '''

        self.canvas.delete(tkinter.ALL)

        self.wall_south = [ [0] * self.maze.N for _ in range(self.maze.N) ]
        self.wall_east  = [ [0] * self.maze.N for _ in range(self.maze.N) ]
        self.tiles      = [ [0] * self.maze.N for _ in range(self.maze.N) ]

        width = self.tile_width + self.wall_width

        for r in range(self.maze.N):
            for c in range(self.maze.N):

                x1 = (c+1)*width+self.wall_width
                y1 = (r+1)*width+self.wall_width
                x2 = (c+2)*width
                y2 = (r+2)*width

                color = self.tile_color(r,c)
                self.tiles[r][c] = self.canvas.create_rectangle(
                    x1,y1, x2,y2,
                    fill=color,
                    width=0
                )

                if self.maze.has_wall(r,c,mz.S): color='black'
                if r+1 < self.maze.N:
                    self.wall_south[r][c] = self.canvas.create_line(
                        (c+1)*width,(r+2)*width, 
                        (c+2)*width,(r+2)*width,
                        fill=color)

                color = self.tile_color(r,c)
                if self.maze.has_wall(r,c,mz.E): color='black'
                if c+1 < self.maze.N:
                    self.wall_east[r][c] = self.canvas.create_line(
                        (c+2)*width,(r+1)*width,
                        (c+2)*width,(r+2)*width,
                        fill=color)

        # exterior walls

        x1 = self.tile_width
        y1 = x1

        x2 = self.tile_width + \
            self.maze.N * self.tile_width + \
            (self.maze.N-1) * self.wall_width + \
            self.wall_width * 3
        y2 = x2

        self.canvas.create_line(x1,y1, x1,y2, fill=self.BORDER_COLOR,width=3*self.wall_width,capstyle=tkinter.ROUND)
        self.canvas.create_line(x2,y1, x2,y2, fill=self.BORDER_COLOR,width=3*self.wall_width,capstyle=tkinter.ROUND)
        self.canvas.create_line(x1,y1, x2,y1, fill=self.BORDER_COLOR,width=3*self.wall_width,capstyle=tkinter.ROUND)
        self.canvas.create_line(x1,y2, x2,y2, fill=self.BORDER_COLOR,width=3*self.wall_width,capstyle=tkinter.ROUND)

    def add_exits_tk_maze(self, r1,c1,r2,c2):
        ''' Creates entrance and exit in ext walls if necessary '''

        width = self.tile_width + self.wall_width

        # handling r1,c1
        if r1 == 0:
            self.canvas.create_line(
                        (c1+1)*width,(r1+1)*width - self.wall_width, 
                        (c1+2)*width,(r1+1)*width - self.wall_width,
                        fill=self.COLORS['START'],
                        width=3*self.wall_width)
        elif r1 == self.maze.N-1:
            self.canvas.create_line(
                        (c1+1)*width,(r1+2)*width + self.wall_width, 
                        (c1+2)*width,(r1+2)*width + self.wall_width,
                        fill=self.COLORS['START'],
                        width=3*self.wall_width)   
        elif c1 == 0:
             self.canvas.create_line(
                        (c1+1)*width - self.wall_width, (r1+1)*width,
                        (c1+1)*width - self.wall_width, (r1+2)*width,
                        fill=self.COLORS['START'],
                        width=3*self.wall_width)
        elif c1 == self.maze.N-1:
            self.canvas.create_line(
                        (c1+2)*width - self.wall_width, (r1+1)*width,
                        (c1+2)*width - self.wall_width, (r1+2)*width,
                        fill=self.COLORS['START'],
                        width=3*self.wall_width)   
        else:
            self.maze.add_tile_state(r1, c1, mz.ST_START)
            self.update_tk_maze(r1, c1)                  
        
        # handling r2,c2
        if r2 == 0:
            self.canvas.create_line(
                        (c2+1)*width,(r2+1)*width - self.wall_width, 
                        (c2+2)*width,(r2+1)*width - self.wall_width,
                        fill=self.COLORS['END'],
                        width=3*self.wall_width)
        elif r2 == self.maze.N-1:
            self.canvas.create_line(
                        (c2+1)*width,(r2+2)*width + self.wall_width, 
                        (c2+2)*width,(r2+2)*width + self.wall_width,
                        fill=self.COLORS['END'],
                        width=3*self.wall_width)   
        elif c2 == 0:
             self.canvas.create_line(
                        (c2+1)*width - self.wall_width, (r2+1)*width,
                        (c2+1)*width - self.wall_width, (r2+2)*width,
                        fill=self.COLORS['END'],
                        width=3*self.wall_width)
        elif c2 == self.maze.N-1:
            self.canvas.create_line(
                        (c2+2)*width - self.wall_width, (r2+1)*width,
                        (c2+2)*width - self.wall_width, (r2+2)*width,
                        fill=self.COLORS['END'],
                        width=3*self.wall_width)
        else:
            self.maze.add_tile_state(r2, c2, mz.ST_END)     
            self.update_tk_maze(r2, c2)                    

    def update_tk_maze(self,r,c,redraw=False):
        '''
        Updates state of a single title, and redraws the change on request. Faster than draw_tk_maze(). 
        '''

        # construct visual representation of a maze on first call
        if len(self.tiles) == 0: self.init_tk_maze()


        # inside walls
        
        color = self.tile_color(r,c)

        # tag_lower avoids chipping joints of existing walls when removing a wall
        if r > 0:
            if self.maze.has_wall(r,c,mz.N):
                self.canvas.itemconfig(self.wall_south[r-1][c], fill='black')
            else:
                self.canvas.itemconfig(self.wall_south[r-1][c], fill=color)
                self.canvas.tag_lower(self.wall_south[r-1][c])

        if r < self.maze.N - 1:
            if self.maze.has_wall(r,c,mz.S):
                self.canvas.itemconfig(self.wall_south[r][c], fill='black')
            else:
                self.canvas.itemconfig(self.wall_south[r][c], fill=color)
                self.canvas.tag_lower(self.wall_south[r][c])

        if c > 0:
            if self.maze.has_wall(r,c,mz.W):
                self.canvas.itemconfig(self.wall_east[r][c-1], fill='black')
            else:
                self.canvas.itemconfig(self.wall_east[r][c-1], fill=color)
                self.canvas.tag_lower(self.wall_east[r][c-1])

        if c < self.maze.N - 1:
            if self.maze.has_wall(r,c,mz.E):
                self.canvas.itemconfig(self.wall_east[r][c], fill='black')
            else:
                self.canvas.itemconfig(self.wall_east[r][c], fill=color)
                self.canvas.tag_lower(self.wall_east[r][c])

        self.canvas.itemconfig(self.tiles[r][c], fill=color)

        if redraw: 
            self.canvas.update()   
            self.sleep()     

    def set_statusbar(self, text):
        self.status.configure(text=text)
        self.status.update()

    def set_delay(self, d):
        self.__delay = d

    def sleep(self):
        time.sleep(self.delay)