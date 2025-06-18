import pygame


class Rune(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load('../graphics/runes/1-32x32.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(center=(x, y))
        self.magnet_radius = 100  # радиус притяжения
        self.magnet_speed = 3
        # Сохраняем ссылку на игрока
        self.player = player

    def update(self):
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
        dx = point[0] - self.rect.centerx
        dy = point[1] - self.rect.centery
        return (dx**2 + dy**2)**0.5
