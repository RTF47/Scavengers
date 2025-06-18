import pygame

class Timer:
    def __init__(self):
        self.start_tick = 0          # момент начала/возобновления
        self.accumulated = 0         # уже пройденное время до паузы
        self.running = False

    def start(self):
        if not self.running:
            self.start_tick = pygame.time.get_ticks()
            self.running = True

    def pause(self):
        if self.running:
            now = pygame.time.get_ticks()
            self.accumulated += now - self.start_tick
            self.running = False

    def resume(self):
        self.start()  # фактически то же, что start, но self.accumulated уже хранит прошлое

    def stop(self):
        if self.running:
            self.pause()
        return self.accumulated

    def get_elapsed(self):
        if self.running:
            return self.accumulated + (pygame.time.get_ticks() - self.start_tick)
        else:
            return self.accumulated
