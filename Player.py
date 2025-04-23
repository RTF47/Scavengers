import pygame
"""
https://gamedevacademy.org/pygame-collisions-tutorial-complete-guide/
"""

class Player:
    def __init__(self,screen):
        pygame.init()
        self.x = 256
        self.y = 256
        self.leftspeed = 4
        self.rightspeed = 4
        self.upspeed = 4
        self.downspeed = 4
        self.rect =pygame.Rect(self.x, self.y, 32, 32)
        self.screen = screen


    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.rect.y -= self.upspeed
        if pressed[pygame.K_DOWN]: self.rect.y += self.downspeed
        if pressed[pygame.K_RIGHT]: self.rect.x += self.rightspeed
        if pressed[pygame.K_LEFT]: self.rect.x -= self.leftspeed


    def draw(self):
        pygame.draw.rect(self.screen,(0, 0, 0), self.rect)


    def collision(self, anotherrect):
        if self.rect.right > 1280:
            self.rect.right = 1280
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720

        # if self.rect.colliderect(anotherrect):
        #     if self.rect.right > anotherrect.left:
        #         self.rect.right = anotherrect.left
        #     if self.rect.left > anotherrect.right:
        #         self.rect.left = anotherrect.right
        #     elif self.rect.top > anotherrect.bottom:
        #         self.rect.top = anotherrect.bottom
        #     elif self.rect.bottom > anotherrect.top:
        #         self.rect.bottom = anotherrect.top

        # pressed = pygame.key.get_pressed()
        # if obs_type == 1 and self.x in range(pos[0]-70, pos[1]+16) and self.y in range(pos[2]-60, pos[3]+1):
        #     self.x = 400
        #     self.y = 300
        # elif obs_type == 2:
        #     if pressed[pygame.K_DOWN]:
        #         if self.x in range(pos[0] - 59, pos[0] + 60) and abs(self.y - pos[1]) == 60:  # top_side
        #             self.downspeed=0
        #
        #     if pressed[pygame.K_UP]:
        #         self.rightspeed = 10
        #         self.leftspeed = 10
        #         self.downspeed=10
        #         if self.x in range(pos[0] - 59, pos[0] + 60) and abs(self.y - pos[1]) == 60:  # bottom_side
        #             self.upspeed = 0
        #
        #     if pressed[pygame.K_RIGHT]:
        #         self.downspeed=10
        #         self.upspeed = 10
        #         self.leftspeed = 10
        #         if self.y in range(pos[1] - 59, pos[1] + 60) and abs(self.x - pos[0]) == 60:  # left_side
        #             self.rightspeed = 0
        #
        #     if pressed[pygame.K_LEFT]:
        #         self.downspeed = 10
        #         self.upspeed = 10
        #         self.rightspeed = 10
        #         if self.y in range(pos[1] - 59, pos[1] + 60) and abs(self.x - pos[0]) == 60:  # right_side
        #             self.leftspeed = 0

