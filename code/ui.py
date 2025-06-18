import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_health(self, current_health, total_health):
        # Заранее загружаем изображения сердечек
        # Убедитесь, что пути к картинкам совпадают с вашими реальными путями
        full_heart = pygame.image.load("../graphics/HP/OneHeart.png").convert_alpha()
        full_heart = pygame.transform.scale(full_heart, (25,24))
        empty_heart = pygame.image.load("../graphics/HP/VoidHeart.png").convert_alpha()
        empty_heart = pygame.transform.scale(empty_heart, (25,24))

        # Сколько всего сердечек хотим отобразить
        self.total_hearts = total_health

        # Задаём начальные координаты для отрисовки (слева сверху)
        start_x = 10
        start_y = 15

        # Отрисовываем каждое сердечко по отдельности
        for i in range(self.total_hearts):
            # Вычисляем позицию сердечка (по горизонтали друг за другом)
            # Можно использовать ширину изображения, чтобы красиво сдвигать каждое следующее
            heart_x = start_x + i * (full_heart.get_width() + 5)
            heart_pos = (heart_x, start_y)

            if i < current_health:
                # Если текущее здоровье ещё не исчерпано — рисуем полное сердечко
                self.display_surface.blit(full_heart, heart_pos)
            else:
                # Иначе — пустое
                self.display_surface.blit(empty_heart, heart_pos)


    def selection_box(self, left, top, has_changed):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        if has_changed:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect


    def weapon_overlay(self,weapon_status, has_changed):
        bg_rect = self.selection_box(10,630, has_changed)
        weapon_surf = self.weapon_graphics[weapon_status]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf,weapon_rect)


    def show_rune(self, player):
        light_image = pygame.image.load("../graphics/runes/1-32x32.png").convert_alpha()
        grey_img = pygame.image.load("../graphics/runes/dark1-32x32.png").convert_alpha()

        if player.has_rune:
            self.display_surface.blit(light_image, (200, 10))
        else:
            self.display_surface.blit(grey_img, (200, 10))


    def display(self,player):
        self.show_health(player.health, player.properties['health'])
        # self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_status, player.can_weap_change)
        # self.selection_box(80,635)
        self.show_rune(player)
