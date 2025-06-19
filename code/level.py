import pygame
from rune import Rune
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from chestL import Chest


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() #Поверхность для отрисовки
        self.visible_sprites = YSortCameraGroup() #Группа видимых спрайтов
        self.obstacle_sprites = pygame.sprite.Group() #Группа спрайтов-препятствий
        self.current_attack = None #Текущая атака
        self.attack_sprites = pygame.sprite.Group() #Группа атакующих спрайтов
        self.attackable_sprites = pygame.sprite.Group() #Группа атакуемых спрайтов

        self.player = None #Игрок

        self.create_map() #Создание игровой карты
        self.ui = UI() #Инициализация пользовательского интерфейса

        self.animation_player = AnimationPlayer() #Аниматор частиц

        self.chest_opening_sound = None #Звук открытия сундука


    def create_map(self):
        """Создает игровой мир из csv файлов, размещает объекты и персонажей."""
        layouts = {
            'boundary': import_csv_layout(BOUNDARY_CSV), #Карта границ
            'entities': import_csv_layout(ENTITY_CSV) #Карта энтити
        }


        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != NOTHING_ID:
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            #Создание невидимых препятствий
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'entities':
                            if col == PLAYER_ID: #Идентификатор игрока
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)
                            else: #Идентификаторы врагов
                                if col == BAMBOO_ID: monster_name = 'bamboo'
                                elif col == SPIRIT_ID: monster_name = 'spirit'
                                elif col == RACCOON_ID: monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.trigger_death_particles)
        #Создание сундука в фиксированной позиции
        self.chest = Chest(CHEST_POS[0],CHEST_POS[1])
        self.visible_sprites.add(self.chest)
        self.obstacle_sprites.add(self.chest)


    def create_attack(self):
        """Создает атакующий спрайт оружия"""
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])


    def destroy_attack(self):
        """Уничтожает текущую атаку"""
        if self.create_attack:
            self.current_attack.kill()
        self.current_attack = None


    def player_attack_logic(self):
        """Обрабатывает логику столкновений атаки с объектами"""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                #Проверка столкновений с атакуемыми объектами
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        #Нанесение урона врагам
                        target_sprite.get_damage(self.player)


    def damage_player(self, amount, attack_type):
        """Наносит урон игроку и запускает анимацию получения урона
        Args:
            amount: Количество отнимаемых сердец.
            attack_type: Тип атаки, относительно сущности.
            """
        if self.player.vulnarable:
            self.player.health -= amount
            self.player.vulnarable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # Создание частиц при получении урона
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])


    def trigger_death_particles(self, pos, particle_type):
        """Активирует частицы смерти в указанной позиции
        Args:
            pos: Позиция частицы, относительно сущности.
            particle_type: Тип партикла, относительно сущности.
            """
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)


    def chest_opening(self):
        """Обрабатывает логику открытия сундука и появления руны"""
        if not self.attackable_sprites:
            if not self.chest.is_opened:
                self.chest.is_opened = True
                self.chest.animation_index = 0
                self.chest.image = self.chest.frames[self.chest.animation_index]
                #Создание руны под сундуком
                self.rune = Rune(self.chest.rect.centerx, self.chest.rect.centery + 70, self.player)
                self.visible_sprites.add(self.rune)


    def run(self, draw_only = False):
        """Основной игровой цикл уровня.

        Args:
            draw_only (bool): Если True, только отрисовывает сцену без обновления логики.
        """
        self.visible_sprites.custom_draw(self.player) #Отрисовка с камерой
        if not draw_only:
            #Обновление игрового состояния
            self.visible_sprites.update() #Обновление всех спрайтов
            self.visible_sprites.enemy_update(self.player) #Специальное обновление врагов
            self.chest_opening() #Проверка открытия сундука
            self.player_attack_logic() #Обработка атак игрока
        self.ui.display(self.player) #Отрисовка интерфейса



class YSortCameraGroup(pygame.sprite.Group):
    """Группа спрайтов с сортировкой по Y-координате и камерой, следующей за игроком"""
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.half_width = self.display_surface.get_size()[0] // 2 #Половина ширины экрана
        self.half_height = self.display_surface.get_size()[1] // 2 #Половина высоты экрана
        self.offset = pygame.math.Vector2(100,200) #Смещение камеры

        #Загрузка фонового изображения
        self.floor_surf = pygame.image.load(MAP).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = OVERLAY_POS)


    def custom_draw(self, player):

        #Расчет смещения камеры
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #Отрисовка фона
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        #Отрисовка спрайтов с сортировкой по Y-координате (имитация глубины)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self,player):
        """Обновляет состояние всех врагов в группе.

        Args:
            player (Player): Целевой объект игрока для AI врагов.
        """
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type =='enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player) #Вызов специального метода обновления врага