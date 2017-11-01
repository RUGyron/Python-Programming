import pygame
import random
import copy
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
        self.randomize = randomize
        self.grid = self.cell_list()
        
    def cell_list(self, randomize=True):
        self.grid = [[Cell(i, j).is_alive() for j in range(self.ncols)] for i in range(self.nrows)]
        if randomize:   
            for i in range(self.nrows):
                for j in range(self.ncols):
                    self.grid[i][j] = Cell(i, j, random.randrange(0, 2)).is_alive()
        return self.grid

    def get_neighbours(self, cell):
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0),
                     (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell[0] + r < self.cell_height and 0 <= cell[1] + c < self.cell_width:
                neighbours.append(self.clist[cell[0] + r][cell[1] + c])
        return neighbours    

    def update(self, clist):
        new_cell_list = deepcopy(clist)
        for i in range(len(clist)):
            for j in range(len(clist[0])):
                summ = sum(CellList.get_neighbours(self, (i, j)))
                if clist[i][j]:
                    if summ < 2 or summ > 3:
                        new_cell_list[i][j] = 0
                else:
                    if summ == 3:
                        new_cell_list[i][j] = 1
        clist = new_cell_list
        return clist
    
    @classmethod

    def __from_file__(self, filename):
        with open(filename) as f:
            self.clist = json.load(f)
        return self.clist

    def __iter__(self):
        self.row_num = 0
        self.col_num = 0
        return self

    def __next__(self):
        cell = self.clist[self.row_num][self.col_num]
        self.col_num += 1
        if self.col_num == self.ncols:
            self.col_num = 0
            self.row_num += 1
        return cell

    def __str__(self):
        string = ''
        for i in self.nrows:
            for j in self.ncols:
                string += Cell(i, j).state
                if len(string) == self.ncols:
                    string += '\n'
        return string

class GameOfLife:
    def __init__(self, width=1280, height=720, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

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
        self.clist = CellList(self.cell_height, self.cell_width).cell_list()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(self.clist)
            self.draw_grid()
            self.clist = CellList.update(self, self.clist)
            pygame.display.flip()
            clock.tick(self.speed) #Breakpoints of a time
            
        pygame.quit()

    def cell_list(self, randomize=True):
        self.clist = CellList(self.cell_height, self.cell_width).cell_list(randomize)
        return self.clist

    def draw_cell_list(self, rects):
        a = self.cell_size
        for i in range(len(rects)):
            for j in range(len(rects[i])):
                if rects[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('red'),
                                     (j * a, i * a, a, a))
                elif rects[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (j * a, i * a, a, a))

    def get_neighbours(self, cell):
        #return CellList(self.cell_height, self.cell_width).get_neighbours()
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0),
                     (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell[0] + r < self.cell_height and 0 <= cell[1] + c < self.cell_width:
                neighbours.append(self.clist[cell[0] + r][cell[1] + c])
        return neighbours
    
    def update_cell_list(self):
        return CellList(self.cell_height, self.cell_width).update_cell_list()
    

if __name__ == '__main__':
    game = GameOfLife(1000, 450, 20)
    game.run()
