import pygame
import random
from pygame.locals import *
from pprint import pprint as pp
from copy import deepcopy


class Cell:
    def __init__(self, row, col, state=0):
        self.alive = state
        self.row = row
        self.col = col

    def is_alive(self):
        return self.alive


class CellList:
    def __init__(self, nrows, ncols, randomize=True):
        self.nrows = nrows
        self.ncols = ncols

        if randomize == 0:
            self.grid = [[Cell(i, j) for j in range(self.ncols)] for i in range(self.nrows)]
        elif randomize:
            self.grid = [[Cell(i, j, random.randrange(0, 2)) for j in range(self.ncols)] for i in range(self.nrows)]

    def get_neighbours(self, cell):
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0),
                     (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell[0] + r < self.nrows and 0 <= cell[1] + c < self.ncols:
                try:
                    neighbours.append(self.grid[cell[0] + r][cell[1] + c].is_alive())
                except:
                    continue
        return neighbours

    def update(self):
        new_cell_list = deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                #print(self.get_neighbours((i, j)))
                summ = sum(c for c in self.get_neighbours((i, j)))
                if self.grid[i][j]:
                    if summ < 2 or summ > 3:
                        new_cell_list[i][j] = 0
                else:
                    if summ == 3:
                        new_cell_list[i][j] = 1
        self.grid = new_cell_list
        return self.grid

    @classmethod
    def from_file(cls, filename):
        new_grid = []
        with open(filename) as f:
            new_grid = [[Cell(i, j, int(value)) for j, value in enumerate(line) if value in '01'] for i, line in
                        enumerate(f)]
        clist_class = cls(len(new_grid), len(new_grid[0]), False)
        clist_class.clist = new_grid
        return clist_class

    def __iter__(self):
        self.row_num = 0
        self.col_num = 0
        return self

    def __next__(self):
        if self.row_num == self.nrows:
            raise StopIteration

        cell = self.grid[self.row_num][self.col_num]
        self.col_num += 1
        if self.col_num == self.ncols:
            self.col_num = 0
            self.row_num += 1
        return cell

    def __str__(self):
        string = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                string += str(Cell(i, j).is_alive())
                if len(string) == self.ncols:
                    string += '\n'
        return string


class GameOfLife:
    def __init__(self, width=1280, height=720, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed

        self.clist = CellList(self.cell_height, self.cell_width, True)
        self.grid = self.clist.grid

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list()
            self.draw_grid()
            self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)  # Breakpoints of a time
        pygame.quit()

    def draw_cell_list(self):
        a = self.cell_size
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j].is_alive() == 1:
                    pygame.draw.rect(self.screen, pygame.Color('gray'),
                                     (j * a, i * a, a, a))
                elif self.grid[i][j].is_alive() == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (j * a, i * a, a, a))

if __name__ == '__main__':
    game = GameOfLife(500, 200, 10)
    game.run()
