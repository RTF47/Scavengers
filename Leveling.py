import pygame
from Obects import Wall, Water, Ground

class Grid:
    def __init__(self, x, y, screen):
        self.firstgrid =           [['w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                                   ['w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
                                   ['w','w','tw','tw','tw','tw','tw','tw','tw','tw','tw','tw','w','w'],
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
        self.groupofrects = []


    def drawing(self):
        for row in self.firstgrid:
            if self.y == 576 and self.x == 576:
                self.y = 128
                self.groupofrects = []
            for col in row:
                if self.x == 576:
                    self.x = 128
                if col == 'w':
                    # print(self.x, self.y)
                    water = Water(self.x, self.y, self.screen)
                    self.groupofrects.append(water.rect)
                    water.draw()
                elif col == 'tw' or col == 'sw':
                    # print(self.x, self.y)
                    wall = Wall(self.x, self.y, self.screen)
                    self.groupofrects.append(wall.rect)
                    wall.draw()
                elif col == 'g':
                    # print(self.x, self.y)
                    ground = Ground(self.x, self.y, self.screen)
                    ground.draw()
                self.x += 32
            self.y += 32
        return
