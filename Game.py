import pygame
from Player import Player
from Obstacle import Obstacle


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.next = self
        self.going = False
        self.screen = pygame.display.set_mode((800,600))
        self.clock = pygame.time.Clock()
        self.player = Player(self.screen)
        self.obstacle1 = Obstacle([100, 100, 100, 200],self.screen,1, (255,0,0), self.player)
        self.obstacle2 = Obstacle([500, 500], self.screen, 2, (0,255,0), self.player)
        # self.walls = [[] in range(10)]
        # walls = [[] for i in range(10)]
        # for i in walls:
        #     for j in range(14):
        #         i.append([])
        # for j in range(0, len(walls)):
        #     for k in range(0, len(walls[j])):
        #         if k == 10:
        #             walls[j][k].append(k * 60)
        #             walls[j][k].append(j * 60)


    def ProcessInput(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.going = True

        self.player.input()


    def Update(self) -> None:
        # self.player.collision([self.obstacle1.x, self.obstacle1.y, self.obstacle1.z, self.obstacle1.w], self.obstacle1.obs_type)
        # self.player.collision([self.obstacle2.x, self.obstacle2.y], self.obstacle2.obs_type)
        self.player.collision()
        self.obstacle2.collision()


    def Render(self) -> None:
        self.screen.fill((255, 255, 255))
        self.obstacle1.draw()
        self.obstacle2.draw()
        self.player.draw()
        pygame.display.flip()


    def SwitchToScene(self, next_scene) -> None:
        self.next = next_scene


if __name__ == '__main__':
    game = Game()
    while not game.going:
        game.ProcessInput()
        game.Update()
        game.Render()
        game.clock.tick(60)
    pygame.quit()
