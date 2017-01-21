import pygame
import sys


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.set_screen()
        self.fps = 60
        self.gameExit = False
        self.clock = pygame.time.Clock()
        self.state = "mainMenu"

        self.mainMenu = Menu(self.screen)
        self.mainMenu.addButton("Play", (self.width/2)-300, 100)
        self.mainMenu.addButton("Options", (self.width/2)-300, 250)
        self.mainMenu.addButton("Rules", (self.width/2)-300, 400)
        self.mainMenu.addButton("Exit", (self.width/2)-300, 550)

        self.playMenu = Menu(self.screen)
        self.playMenu.addButton("Single Player", (self.width/2)-300, 100)
        self.playMenu.addButton("Back", (self.width/2)-300, 250)

        self.spMenu = Menu(self.screen)
        self.spMenu.addLabel("Opponents: ", (self.width/2) - 600, 125)
        self.spMenu.addButton(" 2 ", (self.width/2)-200, 100, 100, 100)
        self.spMenu.addButton(" 3 ", (self.width/2)-50, 100, 100, 100)
        self.spMenu.addButton(" 4 ", (self.width/2)+100, 100, 100, 100)
        self.spMenu.addButton("Back", 340, 250)



    def run(self):
        while not self.gameExit:
            if self.state is "mainMenu":
                self.mainMenu.draw()
            elif self.state is "playMenu":
                self.playMenu.draw()
            elif self.state is "spMenu":
                self.spMenu.draw()

            pygame.display.flip()

            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type is pygame.MOUSEBUTTONUP:
                    if self.state is "mainMenu":
                        if self.mainMenu.buttonList[3]:
                            self.gameExit = True
                        elif self.mainMenu.buttonList[0]:
                            self.state = "playMenu"
                    elif self.state is "playMenu":
                        if self.playMenu.buttonList[1]:
                            self.state = "mainMenu"
                        elif self.playMenu.buttonList[0]:
                            self.state = "spMenu"
                    elif self.state is "spMenu":
                        if self.spMenu.buttonList[3]:
                            self.state = "playMenu"

        pygame.quit()
        sys.exit()

    def set_screen(self, width = 1280, height = 720):
        self.width = width
        self.height = height
        resolution = (width, height)
        self.screen = pygame.display.set_mode(resolution)



class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = (24, 147, 60)
        self.buttonList = []
        self.labelList = []

    def draw(self):
        self.screen.fill(self.background)
        for button in self.buttonList:
            button.draw()
        for label in self.labelList:
            label.draw()

    def addButton(self, text, x, y, width = 600, height = 100):
        self.buttonList.append(MenuButton(self.screen, text, x, y, width, height))

    def addLabel(self, text, posx, posy, size = 50, color = (200, 200, 200)):
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))


class MenuButton:

    def __init__(self, screen, text, posx, posy, width, height):
        """Initialize MenuButton object"""
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.screen = screen
        self.buttonColor = (0, 0, 200)
        self.buttonHighlight = (0, 0, 255)
        self.textColor = (200, 200, 200)
        self.buttonText = text
        self.rect = (posx, posy, width, height)
        self.rectClicked = (posx+10, posy+10, width-20, height-20)

        self.labelContainer = Label(self.screen, text)
        labelposx, labelposy = self._getLabelPosition()
        self.labelContainer.setPosition(labelposx, labelposy)

    def draw(self):
        """Draws the button in its current state"""
        if self.__bool__():
            if pygame.mouse.get_pressed()[0]:  # clicked state
                self.labelContainer.setSize(40)
                labelposx, labelposy = self._getLabelPosition()
                self.labelContainer.setPosition(labelposx ,labelposy)
                pygame.draw.rect(self.screen, self.buttonHighlight, self.rectClicked, 0)  # zero for filled square
                self.labelContainer.draw()
                self.labelContainer.setSize(50)
                labelposx, labelposy = self._getLabelPosition()
                self.labelContainer.setPosition(labelposx ,labelposy)

            else:  # Highlighted state
                pygame.draw.rect(self.screen, self.buttonHighlight, self.rect, 0)  # zero for filled square
                self.labelContainer.draw()
        else:  # Normal state
            pygame.draw.rect(self.screen, self.buttonColor, self.rect, 0)  # zero for filled square
            self.labelContainer.draw()

    def _getLabelPosition(self):
        """Returns two variable which contain the position of the label"""
        labelwidth, labelheight = self.labelContainer.labelObject.get_size()
        labelposx, labelposy = self.posx + ((self.width / 2) - labelwidth / 2), self.posy + ((self.height / 2) - labelheight / 2)
        return labelposx, labelposy


    def __bool__(self):
        """Checks whether mouse position is within button range"""
        mouseX, mouseY = pygame.mouse.get_pos()
        if (mouseX > self.posx and mouseX < (self.posx+self.width)) and (mouseY > self.posy and mouseY < (self.posy+self.height)):
            return True
        else:
            return False


class Label:

    def __init__(self, screen, text, posx = None, posy = None, size = 50, color = (200, 200, 200)):
        """Initialize Label object"""
        self.font = pygame.font.get_default_font()
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.size = size
        self.text = text
        self.color = color
        self.renderer = pygame.font.Font(self.font, self.size)
        self.labelObject = self.renderer.render(self.text, True, self.color)

    def setPosition(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def setSize(self, size):
        self.size = size
        self.renderer = pygame.font.Font(self.font, self.size)
        self.labelObject = self.renderer.render(self.text, True, self.color)

    def draw(self):
        """draw Label object if position is set"""
        if not (self.posx is None or self.posy is None):
            self.screen.blit(self.labelObject, (self.posx, self.posy))
        else:
            print("Position of a label is not set.")

if __name__ == '__main__':
    Game().run()
