import pygame

class Timer:
    def __init__(self):
        self.start_tick = 0          # момент начала/возобновления
        self.accumulated = 0         # уже пройденное время до паузы
        self.running = False

    def start(self):
        """Запуск таймера"""
        if not self.running:
            self.start_tick = pygame.time.get_ticks()
            self.running = True

    def pause(self):
        """Приостановление таймера для паузы"""
        if self.running:
            now = pygame.time.get_ticks()
            self.accumulated += now - self.start_tick
            self.running = False


    def stop(self):
        """Полная остановка таймера для конца игры"""
        if self.running:
            self.pause()
        return self.accumulated

    def get_elapsed(self):
        """Для восстановления таймера после паузы"""
        if self.running:
            return self.accumulated + (pygame.time.get_ticks() - self.start_tick)
        else:
            return self.accumulated
