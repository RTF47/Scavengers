import pygame
from Game import Game

if __name__ == '__main__':
    game = Game()
    while not game.going:
        game.ProcessInput()
        game.Update()
        game.Render()
        game.clock.tick(60)
    pygame.quit()