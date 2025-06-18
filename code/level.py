import pygame
from rune import Rune
from settings import *
from tile import Tile
from player import Player
from debug import player_cords
from support import import_csv_layout
from random import randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from chestL import Chest


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.player = None

        self.create_map()
        self.ui = UI()

        self.animation_player = AnimationPlayer()

        self.chest_opening_sound = None

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_Boundary.csv'),
            'entities': import_csv_layout('../map/map_Entitys.csv')
        }


        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.trigger_death_particles)
        self.chest = Chest(1216, 1792)
        self.visible_sprites.add(self.chest)
        self.obstacle_sprites.add(self.chest)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.create_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 60)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player)

    def damage_player(self, amount, attack_type):
        if self.player.vulnarable:
            self.player.health -= amount
            self.player.vulnarable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def chest_opening(self):
        if self.attackable_sprites:
            if not self.chest.is_opened:
                self.chest.is_opened = True
                self.chest.animation_index = 0
                self.chest.image = self.chest.frames[self.chest.animation_index]
                self.rune = Rune(self.chest.rect.centerx, self.chest.rect.centery + 70, self.player)
                self.visible_sprites.add(self.rune)

    def run(self, draw_only = False):
        self.visible_sprites.custom_draw(self.player)
        # Исправленная строка:
        if not draw_only:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.chest_opening()
            self.player_attack_logic()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.half_width = self.display_surface.get_size()[0] // 2
            self.half_height = self.display_surface.get_size()[1] // 2
            self.offset = pygame.math.Vector2(100,200)

            self.floor_surf = pygame.image.load('../graphics/tilemap/Map3.png').convert()
            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

        def custom_draw(self, player):
            self.offset.x = player.rect.centerx - self.half_width
            self.offset.y = player.rect.centery - self.half_height

            floor_offset_pos = self.floor_rect.topleft - self.offset
            self.display_surface.blit(self.floor_surf, floor_offset_pos)

            # for sprite in self.sprites():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        def enemy_update(self,player):
            enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type =='enemy']
            for enemy in enemy_sprites:
                enemy.enemy_update(player)