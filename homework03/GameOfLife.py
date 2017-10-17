import pygame
import random
import copy
from pygame.locals import *
from pprint import pprint as pp
from copy import deepcopy

class GameOfLife:
    def __init__(self, width = 1280, height = 720, cell_size = 10, speed = 300):
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
        self.clist = game.cell_list()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(self.clist)
            self.draw_grid()
            self.clist = self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


    def cell_list(self, randomize=True):
        width = self.cell_width
        height = self.cell_height
        clist = [[0 for i in range(width)] for j in range(height)]
        if randomize:
            for i in range(height):
                for j in range(width):
                    clist[i][j] = random.randrange(0,2)
        return clist


    def draw_cell_list(self, rects):
        a = self.cell_size
        for i in range(len(rects)):
            for j in range(len(rects[i])):
                if rects[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('gray'), (j * a, i * a, a, a))
                elif rects[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (j * a, i * a, a, a))
                    
                    
    def get_neighbours(self, cell):
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell[0] + r < self.cell_height and 0 <= cell[1] + c < self.cell_width:
                neighbours.append(self.clist[cell[0] + r][cell[1] + c])
        return neighbours
        
    
    def update_cell_list(self, cell_list):
        new_cell_list = deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                summ = sum(self.get_neighbours((i, j)))
                if self.clist[i][j]:
                    if summ < 2 or summ > 3:
                        new_cell_list[i][j] = 0
                else:
                    if summ == 3:
                        new_cell_list[i][j] = 1
        self.clist = new_cell_list
        return self.clist      
          
        
        
if __name__ == '__main__':
    game = GameOfLife(800, 600, 10)
    game.run()