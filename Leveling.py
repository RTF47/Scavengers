import pygame
import numpy as np
from Obects import Wall, Water, Ground

class Grid():
    def __init__(self, x, y, screen):
        self.firstgrid =           [['w','w','w','w','w','w','w','w','w','w''w','w','w','w'],
                                   ['w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                                   ['w','w','fw','fw','fw','fw','fw','fw','fw','fw','fw','fw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','sw','g','g','g','g','g','g','g','g','sw','w','w'],
                                   ['w','w','tw','tw','tw','tw','tw','tw','tw','tw','tw','tw','w','w'],
                                   ['w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                                   ['w','w','w','w','w','w','w','w','w','w','w','w','w','w']]
        self.screen = screen
        self.x = x
        self.y = y
        self.water = Water(self.x, self.y, self.screen)
        self.wall = Wall(self.x, self.y, self.screen)
        self.ground = Ground(self.x, self.y, self.screen)


    def drawing(self):
        for row in self.firstgrid:
            for col in row:
                if col == 'w':
                    self.water.draw()
                elif col == 'tw' or col == 'sw':
                    self.wall.draw()
                elif col == 'g':
                    self.ground.draw()
                self.x += 32
            self.y += 32
