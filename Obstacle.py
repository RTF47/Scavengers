import pygame

class Obstacle:
    def __init__(self, pos: list, surface, obs_type, color: tuple, Player):
        self.obs_type = obs_type
        if obs_type == 1:
            self.x = pos[0]
            self.y = pos[1]
            self.z = pos[2]
            self.w = pos[3]
        elif obs_type == 2:
            self.x = pos[0]
            self.y = pos[1]
            self.rect = pygame.Rect(self.x,self.y, 15,60)
        self.color = color
        self.screen = surface
        self.player = Player


    def draw(self):
        if self.obs_type == 1:
            pygame.draw.line(self.screen, self.color, (self.x,self.y),(self.z,self.w), width=20)
        elif self.obs_type == 2:
            pygame.draw.rect(self.screen, self.color, self.rect)

    def collision(self):
        pressed = pygame.key.get_pressed()
        if self.player.rect.colliderect(self.rect):
            if self.player.rect.right >= self.rect.left and self.player.rect.right <= self.rect.right and pressed[pygame.K_RIGHT]:
                self.player.rect.right = self.rect.left

            if self.player.rect.left <= self.rect.right and self.player.rect.left >= self.rect.left and pressed[pygame.K_LEFT]:
                self.player.rect.left = self.rect.right

            if self.player.rect.bottom >= self.rect.top and self.player.rect.bottom <= self.rect.bottom and pressed[pygame.K_DOWN]:
                self.player.rect.bottom = self.rect.top

            if self.player.rect.top <= self.rect.bottom and self.player.rect.top >= self.rect.top and pressed[pygame.K_UP]:
                self.player.rect.top = self.rect.bottom
        print(self.player.rect.left, self.player.rect.top)





