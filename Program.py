import pygame, sys
from pygame import gfxdraw

class Game:
    def __init__(self):
        pygame.init()

        self.width = 1280
        self.height = 720
        self.fps = 30
        self.gameExit = False
        self.clock = pygame.time.Clock()
        self.resolution = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.resolution)

    def run(self):
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True

            MainMenu(self.screen).draw()
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()





class MainMenu:

    def __init__(self, screen):
        self.screen = screen
        self.background = (24, 147, 60)

    def draw(self):
        self.screen.fill(self.background)



if __name__ == '__main__':
    Game().run()
