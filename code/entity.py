import pygame
from math import sin
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        """Класс-шаблон для всех энтити на карте
        Args:
            groups: Группы, которые наследует класс.
        """
        super().__init__(groups)
        self.frame_index = FRAME_IND
        self.frame_animation_speed = FRAME_SPEED
        self.direction = pygame.math.Vector2()


    def move(self, speed):
        """Передвижение энтити
        Args:
            speed: Скорость энтити.
        """
        if self.direction.magnitude() != 0:
            """Фиксим движение по диагонали 
            (исходя из теоремы пифагора, где катеты Ox и Oy всегда меньше гипотинузы (Oxy), а у нас должны быть равны)"""
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        """Столкновение с объектами группы self.obstacle_sprites в двух направлениях (Ox,Oy)
        Args:
            direction: Направление энтити.
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x>0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        """Используется для создания эффекта мерцания спрайта"""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
