import pygame, sys
from pygame import gfxdraw

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.width = 1280
        self.height = 720
        self.fps = 60
        self.gameExit = False
        self.clock = pygame.time.Clock()
        self.createWindow()


    def run(self):
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
            mainmenu = MainMenu(self.screen)
            mainmenu.draw()
            if mainmenu.exit.isClicked():
                self.gameExit = True

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

    def createWindow(self, captions = "Project 3"):
        self.resolution = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(captions)






class MainMenu:

    def __init__(self, screen):
        self.screen = screen
        self.background = (24, 147, 60)

    def draw(self):
        x, y = pygame.display.get_surface().get_size()
        self.screen.fill(self.background)
        self.play = MainMenuButton(self.screen, "Play", (x/2) - 300, 150)
        self.options = MainMenuButton(self.screen, "Options", (x / 2) - 300, 300)
        self.rules = MainMenuButton(self.screen, "Rules", (x / 2) - 300, 450)
        self.exit = MainMenuButton(self.screen, "Exit", (x / 2) - 300, 600)

        self.play.draw()
        self.options.draw()
        self.rules.draw()
        self.exit.draw()

class MainMenuButton:

    def __init__(self, screen, text, posx, posy, width = 600, height = 100):
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.screen = screen
        self.buttonColor = (0, 0, 200)
        self.buttonHighlight = (0, 0, 255)
        self.textColor = (100, 100, 100)
        self. buttonText = text
        self.rect = (posx, posy, width, height)
        self.rectClicked = (posx+50, posy, width-100, height)

        self.font = pygame.font.get_default_font()
        self.renderer = pygame.font.Font(self.font, 50)

    def draw(self):

        mouseX, mouseY = pygame.mouse.get_pos()
        if (mouseX > self.posx and mouseX < (self.posx+self.width)) and (mouseY > self.posy and mouseY < (self.posy+self.height)):
            if self.isClicked():
                label = self.renderer.render(self.buttonText, True, self.textColor)
                x, y = label.get_size()
                pygame.draw.rect(self.screen, self.buttonHighlight, self.rectClicked, 0)  # zero for filled square
                self.screen.blit(label, (self.posx + ((self.width / 2) - x / 2), self.posy + ((self.height / 2) - y / 2)))
            else:
                label = self.renderer.render(self.buttonText, True, self.textColor)
                x, y = label.get_size()
                pygame.draw.rect(self.screen, self.buttonHighlight, self.rect, 0)  # zero for filled square
                self.screen.blit(label, (self.posx + ((self.width / 2) - x / 2), self.posy + ((self.height / 2) - y / 2)))
        else:
            label = self.renderer.render(self.buttonText, True, self.textColor)
            x, y = label.get_size()
            pygame.draw.rect(self.screen, self.buttonColor, self.rect, 0) # zero for filled square
            self.screen.blit(label, (self.posx+((self.width/2)-x/2), self.posy+((self.height/2)-y/2)))

    def isClicked(self):

        mouseX, mouseY = pygame.mouse.get_pos()
        if (mouseX > self.posx and mouseX < (self.posx+self.width)) and (mouseY > self.posy and mouseY < (self.posy+self.height)):
            if pygame.mouse.get_pressed()[0]:
                return True
            else:
                return False





if __name__ == '__main__':
    Game().run()
