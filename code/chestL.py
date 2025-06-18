import pygame

from support import *


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.recsaling(import_folder('../graphics/chest'))
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-60,-90)

        self.is_opened = False
        self.animation_index = 0
        self.last_update_time = pygame.time.get_ticks()


    def update(self,player=None):
        if self.is_opened:
            now = pygame.time.get_ticks()
            # Переключаем кадры анимации с небольшим интервалом
            if now - self.last_update_time > 100:
                self.last_update_time = now
                if self.animation_index < len(self.frames) - 1:
                    self.animation_index += 1
                    self.image = self.frames[self.animation_index]
        else:
            self.image = self.frames[0]


    def recsaling(self, frames):
        final = []
        for i in frames:
            final.append(pygame.transform.scale(i, (128, 128)))
        return final