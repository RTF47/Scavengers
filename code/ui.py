import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #загружаем спрайты оружий
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)


    def show_health(self, current_health, total_health):
        """Показываем ХП
        Args:
            current_health: Текущее количество ХП.
            total_health: Общее количество ХП.
        """
        full_heart = pygame.image.load(F_HEART).convert_alpha()
        full_heart = pygame.transform.scale(full_heart, HEART_SIZE)
        empty_heart = pygame.image.load(E_HEART).convert_alpha()
        empty_heart = pygame.transform.scale(empty_heart, HEART_SIZE)

        # Сколько всего сердечек
        self.total_hearts = total_health

        # Задаём начальные координаты для отрисовки (слева сверху)
        start_x = HEART_POS[0]
        start_y = HEART_POS[1]

        # Отрисовываем каждое сердечко
        for i in range(self.total_hearts):
            # Вычисляем позицию сердечка (по горизонтали друг за другом)
            heart_x = start_x + i * (full_heart.get_width() + HEART_GAP)
            heart_pos = (heart_x, start_y)

            if i < current_health:
                # Если текущее здоровье ещё не исчерпано — рисуем полное сердечко
                self.display_surface.blit(full_heart, heart_pos)
            else:
                # Иначе — пустое
                self.display_surface.blit(empty_heart, heart_pos)


    def selection_box(self, left, top, has_changed):
        """Отрисовка слота для оружия
        Args:
            left: Позиция на экране относительно левой границы.
            top: Позиция на экране относительно верхней границы.
            has_changed: Поменял ли оружие.
        """
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, SBOX_WIDTH)
        if has_changed:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, SBOX_WIDTH)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, SBOX_WIDTH)
        return bg_rect


    def weapon_overlay(self,weapon_status, has_changed):
        """Отрисовка оружия в слоте
        Args:
            weapon_status: Статус оружия.
            has_changed: Поменял ли оружие.
        """
        bg_rect = self.selection_box(WEAPON_POS[0],WEAPON_POS[1], has_changed)
        weapon_surf = self.weapon_graphics[weapon_status]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf,weapon_rect)


    def show_rune(self, player):
        """Отрисовывем наличие/отсутствие руны
        Args:
            player: Игрок.
        """
        light_image = pygame.image.load(RUNE_PATH).convert_alpha()
        grey_img = pygame.image.load(E_RUNE_PATH).convert_alpha()

        if player.has_rune:
            self.display_surface.blit(light_image, RUNE_UI_POS)
        else:
            self.display_surface.blit(grey_img, RUNE_UI_POS)


    def display(self,player):
        """Отрисовываем весь UI
        Args:
            player: Игрок.
        """
        self.show_health(player.health, player.properties['health'])
        self.weapon_overlay(player.weapon_status, player.can_weap_change)
        self.show_rune(player)
