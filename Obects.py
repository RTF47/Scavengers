import pygame

class Wall():
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 32,32)
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
        

    def collison(self):
        pass


class Water():
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 32,32)
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen, (30,144,255), self.rect)


    def collision(self):
        pass


class Ground():
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 32,32)
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen, (45,175,20), self.rect)
