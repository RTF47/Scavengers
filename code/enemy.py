import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particels):
        """Класс-шаблон для врага
        Args:
            monster_name: Имя для врага.
            pos: Позиция врага.
            groups: Группы, которые наследует класс.
            obstacle_sprites: Группа, определяющая коллизию класса.
            damage_player: Метод, обрабатывающий урон к игроку.
            trigger_death_particels: Метод, определяющий партиклы после смерти.
        """
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #Параметры спрайта
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #Главные параметры, описываемые врага
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # Переменные, применяемые для расчёта получения/не получения и нанесения урона
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = ATTACK_CD
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particels
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = INVICIBILITY_DUR

        #Звуки
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound = pygame.mixer.Sound(DEATH_S)
        self.hit_sound = pygame.mixer.Sound(HIT_S)
        self.enemy_sound_volume = ENEMY_V
        self.attack_sound.set_volume(self.enemy_sound_volume)
        self.death_sound.set_volume(self.enemy_sound_volume)
        self.hit_sound.set_volume(self.enemy_sound_volume)



    def import_graphics(self, name):
        """Импорт спрайтов для анимации ходьбы, стояния и атаки врага
        Args:
            name: Название врага.
        """
        self.animations = {'idle':[], 'move':[], 'attack':[]}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)


    def get_player_distance_direction(self,player):
        """Получение дистанции и направления до игрока
        Args:
            player: Игрок.
        """
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        return distance, direction


    def get_status(self, player):
        """Также, как и в классе player - получение статуса врага (идет, стоит, атакует)
        Args:
            player: Игрок.
        """
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = FRAME_IND
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'


    def actions(self, player):
        """Атака и передвижение врага к игроку
        Args:
            player: Игрок.
        """
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()


    def animate(self):
        """Анимация ходьбы, атаки и тд врага"""
        animation = self.animations[self.status]
        self.frame_index += self.frame_animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = FRAME_IND
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def cooldown(self):
        """Кулдаун атаки врага (зависимость от vulnerable - уязвимости)"""
        current_time = pygame.time.get_ticks()
        if not self.can_attack:

            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True


    def get_damage(self,player):
        """Получение урона врагом
        Args:
            player: Игрок.
        """
        if self.vulnerable:
            self.hit_sound.play()
            self.get_player_distance_direction(player)[1]
            self.health -= player.get_full_weapon_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False


    def check_death(self):
        """Обработка смерти врага"""
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.death_sound.play()


    def hit_reaction(self):
        """Отбрасывание врага после удара игроком"""
        if not self.vulnerable:
            self.direction *= -self.resistance


    """Разделение update на два метода было сделано для корректной работы в level.update()"""
    def update(self,player=None):
        """Метод update, независимый от игрока"""
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()


    def enemy_update(self, player):
        """Метод update, зависимый от игрока
        Args:
            player: Игрок.
        """
        self.get_status(player)
        self.actions(player)

