import pygame
import sys


class Game:
    def __init__(self):
        # Init pygame
        pygame.init()
        pygame.font.init()
        self.set_screen()
        self.fps = 60
        self.gameExit = False
        self.clock = pygame.time.Clock()

        # Init game
        self.screenList =[]

        # Init screens
        self.initScreens()

    def run(self):
        while not self.gameExit:
            # Display pygame screen
            for mainScreen in self.screenList:  # For all main screens
                for subScreen in mainScreen:    # For all subscreens within main screens (for convenience a mainscreen is also considered subscreen)
                    if self.state is subScreen: # Filter out the pygame screen that should be active (the var self.state is changed through menu buttons)
                        subScreen.draw()        # Draw that screen

            self.t.get_label().draw()

            pygame.display.flip()

            # Update pygame screen
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type is pygame.MOUSEBUTTONUP:
                    self.buttonFunctions()
                    self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]

        # Exit if self.gameExit
        pygame.quit()
        sys.exit()

    # Methods
    def set_screen(self, width = 1280, height = 720):
        self.width = width
        self.height = height
        resolution = (width, height)
        self.screen = pygame.display.set_mode(resolution)

    def initScreens(self):
        # Screens are in a list, so that scrolling through screens is not hardcoded.
        # 2d list because we make a distinction between main screens and subscreens:
        #   Main screens can take you further in the main screen list and also allows you to access its own subscreens
        #   A subscreen is a screen that belongs to a main screen, you access it through its mainscreen.
        #   When you exit the subscreen you go back to its main screen.
        #
        # For all buttons in the addButton list,
        #   the first button in the list takes you further in the main screen list
        #   The last button in the list takes you a screen backwards.
        #   Screens in between take you to subscreens
        #   (TO BE CODED: a subscreen does not require a 'first button that takes you forward')
        #
        # init main screen: Main Menu
        self.screenList.append([])  # Make room for new screen
        self.screenList[0].append(Menu(self.screen))  # Insert mainScreen#  (class object in list.)
        self.screenList[0][0].addLabel("Question: ", int(self.width / 8), 25)
        self.screenList[0][0].addButton("A", int(self.width / 8), 200)  # Add buttons to the screen
        self.screenList[0][0].addLabel("Answer A: ", int(self.width / 2.75), 200, size=20)
        self.screenList[0][0].addButton("B", int(self.width / 8), 350)
        self.screenList[0][0].addLabel("Answer B: ", int(self.width / 2.75), 350, size=20)
        self.screenList[0][0].addButton("C", int(self.width / 8), 500)
        self.screenList[0][0].addLabel("Answer C: ", int(self.width / 2.75), 500, size=20)

        self.t = Timer(self.screen)
        # Init set screen to be active on default
        self.activeMainScreen = 0
        self.activeSubScreen = 0
        self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]

    def buttonFunctions(self):
        if self.state is self.screenList[0][0]:
            if self.state.buttonList[0]:
                print("Wrong!")
            elif self.state.buttonList[1]:
                print("Wrong!")
            elif self.state.buttonList[2]:
                print("Right!")
        else:
            if (len(self.state.buttonList)) > 0:  # if more than 1 button
                if self.state.buttonList[0]:  # if button is pressed
                    self.activeMainScreen += 1  # go a main screen forward
                    self.activeSubScreen = 0
            if (len(self.state.buttonList)) > 1:
                if self.state.buttonList[-1]:
                    if self.activeSubScreen == 0:
                        if self.activeMainScreen == 0:
                            self.gameExit = True
                        else:
                            self.activeMainScreen -= 1
                            self.activeSubScreen = 0
                    else:
                        self.activeSubScreen = 0
            if (len(self.state.buttonList) - 2) >= 0:  # if more than 2 buttons
                for i in range(len(self.state.buttonList) - 1):
                    if self.state.buttonList[i]:
                        self.activeSubScreen = i


class playScreen:
    def __init__(self, screen):
        self.screen = screen
        #self.nrPlayers = 4
        self.background = pygame.image.load("res/spelbord.jpg")
        self.backgroundtransformed = pygame.transform.scale(self.background, (int(1280 * 0.5), int(720) - 200))
        self.buttonList = []
        self.labelList = []
        self.playerList = []
        self.actionList = []

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.backgroundtransformed, (1280 / 4, 100))

        for button in self.buttonList:
            button.draw()
        for label in self.labelList:
            label.draw()

    def addButton(self, text, posx, posy, width = 600, height = 100):
        self.buttonList.append(MenuButton(self.screen, text, posx, posy, width, height))

    def addLabel(self, text, posx, posy, size = 50, color = (200, 200, 200)):
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))

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

    def addButton(self, text, posx, posy, width = 275, height = 75):
        self.buttonList.append(MenuButton(self.screen, text, posx, posy, width, height))

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
        self.labelContainer = Label(self.screen, self.buttonText)
        labelposx, labelposy = self._getLabelPosition()
        self.labelContainer.setPosition(labelposx, labelposy)
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
class Timer:
    def __init__(self, screen, posx = 0, posy = 0):
        self.posx = posx
        self.posy = posy
        self.time = pygame.time.get_ticks()
        self.screen = screen
        pass

    def get_time(self):
        return int(pygame.time.get_ticks() - self.time)

    def get_label(self):
        return Label(self.screen, str(int(self.get_time()/1000)), self.posx, self.posy)

    def reset(self):
        self.time = pygame.time.get_ticks()




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
