import pygame

from settings import *
from support import import_folder

class AnimationPlayer:
    """Импорт спрайтов для анимации партиклов"""
    def __init__(self):
        #Импорт всех спрайтов для создания анимации партикла
        self.frames = {
            # attacks
            'claw': import_folder(CLAW_F),
            'slash': import_folder(SLASH_F),
            'sparkle': import_folder(SPARKLE_F),
            'leaf_attack': import_folder(LEAF_F),
            'thunder': import_folder(THENDER_F),

            # monster deaths
            'squid': import_folder(SQUID_D),
            'raccoon': import_folder(RACCOON_D),
            'spirit': import_folder(SPIRIT_D),
            'bamboo': import_folder(BAMBOO_D)}


    def create_particles(self, animation_type, pos, groups):
        """Создание парктикла"""
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)



class ParticleEffect(pygame.sprite.Sprite):
    """Класс-шаблон для создания партикла"""
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = FRAME_IND
        self.animation_speed = FRAME_SPEED
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        """Анимация партикла"""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """Полный метод апдейта всех смежных методов"""
        self.animate()