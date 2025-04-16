import pygame
import numpy as np
from Obects import Wall, Water, Ground

class Grid():
    def __init__(self, x, y, screen):
        self.firstgrid = [['w','w','w','w','w','w','w','w','w','w''w','w','w','w'],
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


    def drawing(self):
        for row in self.firstgrid:
            for col in row:
                if col == 'w':
                    water = Water(self.x, self.y, self.screen)
                    water.draw()
                if col == 'tw' or col == 'sw':
                    wall = Wall(self.x, self.y, self.screen)
                    wall.draw()
                if col == 'g':
                    ground = Ground(self.x, self.y, self.screen)
                    ground.draw()
                self.x += 32
            self.y += 32


