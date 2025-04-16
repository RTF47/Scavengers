import pygame
from Leveling import Grid

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.going = False
        self.screen = pygame.display.set_mode((1280,720))
        self.level = Grid(128, 128, self.screen)
        self.clock = pygame.time.Clock()


    def ProcessInput(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.going = True

        # self.player.input()


    def Update(self) -> None:
        pass


    def Render(self) -> None:
        self.screen.fill((255, 255, 255))
        #player
        self.level.drawing()
        pygame.display.flip()


    def SwitchToScene(self, next_scene) -> None:
        #self.next = next_scene
        pass



