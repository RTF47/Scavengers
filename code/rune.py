import pygame
from settings import *

class Rune(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        """Класс, создающий руну
        Args:
            x: Позиция руны по x.
            y: Позиция руны по y.
            player: Игрок.
        """
        super().__init__()
        self.image = pygame.image.load(RUNE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(center=(x, y))
        self.magnet_radius = RUNE_RADIUS  # радиус притяжения
        self.magnet_speed = RUNE_SPEED
        self.player = player


    def update(self):
        """Обработка всех смежных событий для руны"""
        # Поиск игрока в радиусе
        distance = self.distance_to(self.player.rect.center)
        if distance < self.magnet_radius:
            # Движемся по направлению к игроку
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            length = max(1, (dx**2 + dy**2)**0.5)
            dx /= length
            dy /= length
            self.rect.x += dx * self.magnet_speed
            self.rect.y += dy * self.magnet_speed

        # Проверяем столкновение с игроком
        if self.rect.colliderect(self.player.rect):
            self.player.has_rune = True
            self.kill()
            print('yes')


    def distance_to(self, point):
        """Расчёт дистанции до игрока
        Args:
            point (List): Позиция игрока.
        """
        dx = point[0] - self.rect.centerx
        dy = point[1] - self.rect.centery
        return (dx**2 + dy**2)**0.5
