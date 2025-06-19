import pygame
from support import *


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Класс-шаблон для сундука
        Args:
            x: Позиция относительно Ох.
            y: Позиция относительно Оу.
        """
        super().__init__()
        #Параметры спрайта
        self.frames = self.recsaling(import_folder('../graphics/chest'))
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-60,-90)

        self.is_opened = False #Проверка открыт или еще нет
        self.animation_index = 0 #Начальный индекс кадра для анимации открытия
        self.last_update_time = pygame.time.get_ticks() #Последний тик, используемый для окончания анимации


    def update(self,player=None):
        """Логика открытия сундука + анимация"""
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
        """Увеличение размера всех кадров сундука
        Args:
            frames (List): Список кадров для анимации.
        """
        final = []
        for i in frames:
            final.append(pygame.transform.scale(i, (128, 128)))
        return final