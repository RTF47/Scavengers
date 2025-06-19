import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    """Импорт спрайтов для анимации партиклов"""
    def __init__(self):
        #Импорт всех спрайтов для создания анимации партикла
        self.frames = {
            # attacks
            'claw': import_folder('../graphics/particles/claw'),
            'slash': import_folder('../graphics/particles/slash'),
            'sparkle': import_folder('../graphics/particles/sparkle'),
            'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
            'thunder': import_folder('../graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('../graphics/particles/smoke_orange'),
            'raccoon': import_folder('../graphics/particles/raccoon'),
            'spirit': import_folder('../graphics/particles/nova'),
            'bamboo': import_folder('../graphics/particles/bamboo')}


    def create_particles(self, animation_type, pos, groups):
        """Создание парктикла"""
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)



class ParticleEffect(pygame.sprite.Sprite):
    """Класс-шаблон для создания партикла"""
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
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