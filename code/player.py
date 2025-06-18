import pygame
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6,-26)

        self.import_player_assets()
        self.status = 'down'

        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack

        self.destroy_attack = destroy_attack
        self.weapon_status = 0
        self.weapon = list(weapon_data.keys())[self.weapon_status]
        self.can_weap_change = True
        self.weapon_change_time = None
        self.change_cooldown = 200

        self.properties = {'health':6, 'energy':60,'attack':10, 'speed':6}
        self.health = self.properties['health']
        self.exp = 123
        self.speed = self.properties['speed']

        self.vulnarable = True
        self.hurt_time = None
        self.invulnarability_duration = 500

        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.attack_sound_volume = 0.2
        self.weapon_attack_sound.set_volume(self.attack_sound_volume)

        self.has_rune = False


    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'right_idle':[], 'left_idle':[], 'down_idle':[], 'up_idle':[],
            "right_attack":[], 'left_attack':[], 'up_attack':[], 'down_attack':[]
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            if keys[pygame.K_q] and self.can_weap_change:
                self.can_weap_change = False
                self.weapon_change_time = pygame.time.get_ticks()

                if self.weapon_status < len(list(weapon_data.keys())) -1:
                    self.weapon_status +=1
                else:
                    self.weapon_status = 0
                self.weapon = list(weapon_data.keys())[self.weapon_status]


    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        if not self.can_weap_change:
            if current_time - self.weapon_change_time >= self.change_cooldown:
                self.can_weap_change = True
        if not self.vulnarable:
            if current_time - self.hurt_time >= self.invulnarability_duration:
                self.vulnarable = True


    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.frame_animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnarable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def get_full_weapon_damage(self):
        base_damage = self.properties['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage


    def update(self,player=None):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)