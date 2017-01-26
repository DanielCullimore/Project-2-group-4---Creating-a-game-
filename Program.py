import pygame
import sys
from random import *
import math


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.set_screen()
        self.fps = 60
        self.gameExit = False
        self.clock = pygame.time.Clock()
        self.screenList =[]
        self.whoseTurn = 0
        self.nrPlayers = 4
        self.tempTurn = False
        self.whoseTempTurn = 0

        #MAIN MENU
        self.screenList.append([]) # Make room for new screen
        self.screenList[0].append(Menu(self.screen)) # Insert mainScreen (class object in list.)
        self.screenList[0][0].addButton("Play", (self.width/2)-300, 100) # Add buttons to the screen
        self.screenList[0][0].addButton("Options", (self.width/2)-300, 250)
        self.screenList[0][0].addButton("Rules", (self.width/2)-300, 400)
        self.screenList[0][0].addButton("Exit", (self.width/2)-300, 550)
        # OPTIONS SCREEN
        self.screenList[0].append(Menu(self.screen)) # insert subScreen (class object in list.)
        self.screenList[0][1].addButton("Psuedo Play", -100, -100)
        self.screenList[0][1].addButton("Back", (self.width / 2) - 300, 550)
        # RULES SCREEN
        self.screenList[0].append(Menu(self.screen))
        self.screenList[0][2].addButton("Psuedo Play", -100, -100)
        self.screenList[0][2].addButton("Back", (self.width / 2) - 300, 550)

        #PLAY MENU
        self.screenList.append([])  # Make room for new screen
        self.screenList[1].append(Menu(self.screen))
        self.screenList[1][0].addButton("Single Player", (self.width/2)-300, 100)
        self.screenList[1][0].addButton("Back", (self.width/2)-300, 250)

        #SINGLE PLAYER MENU
        self.screenList.append([])  # Make room for new screen
        self.screenList[2].append(Menu(self.screen))
        self.screenList[2][0].addButton("Play", (self.width / 2) - 300, 100)
        self.screenList[2][0].addLabel("Players = 4", (self.width/2) - 600, 300)
        # self.screenList[2][0].addPlayerButton(" 2 ", (self.width/2)-200, 300, 100, 100)
        self.screenList[2][0].addButton("Back", 340, 450)

        #Play screen
        self.screenList.append([])  # Make room for new screen
        self.screenList[3].append(playScreen(self.screen))
        self.screenList[3][0].addButton("Psuedo Play", -100, -100)
        self.screenList[3][0].addButton("Options", (self.width) - 255, 75, 270,75)
        self.screenList[3][0].addButton("Psuedo Exit", -100, -100)
        self.screenList[3][0].addPlayer( (255, 0, 0), "Red Bob", 337, self.height-100)
        self.screenList[3][0].addPlayer( (0, 255, 0), "Green Frank", 337+160, self.height-100)
        self.screenList[3][0].addPlayer( (0, 0, 255), "Blue Mike", 337+(160*2), self.height-100)
        self.screenList[3][0].addPlayer( (255, 0, 255), "Magenta Fox",  337+(160*3), self.height-100)
        self.screenList[3][0].addDice("Dice",50,50)
        self.direction = 0
        self.screenList[3][0].addDirection("Direction", 150, 50)
        # Subscreen pauze game
        self.screenList[3].append(Menu(self.screen))
        self.screenList[3][1].addButton("Psuedo Play", -100, -100)
        self.screenList[3][1].addButton("Continue", (self.width / 2) - 300, 100)
        self.screenList[3][1].addButton("Exit", (self.width / 2) - 300, 550)

        #DEFAULT ACTIVE SCREEN
        self.activeMainScreen = 0
        self.activeSubScreen = 0
        self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]

    def run(self):
        while not self.gameExit:
            for mainScreen in self.screenList:
                # Loop over screenList[mainScreen][Y]
                for subScreen in mainScreen:
                    if self.state is subScreen:
                        subScreen.draw() #DRAW SCREENS

            pygame.display.flip()

            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type is pygame.MOUSEBUTTONUP:
                    if (len(self.state.buttonList)) > 0: # if more than 1 button
                        if self.state.buttonList[0]: # if button is pressed
                            self.activeMainScreen += 1
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
                    if (len(self.state.buttonList)-2) >= 0: # if more than 2 buttons
                        for i in range(len(self.state.buttonList)-1):
                            if self.state.buttonList[i]:
                                self.activeSubScreen = i

                    if self.screenList[3][0].dice:
                        self.diceNumber = randint(1,6)
                        self.screenList[3][0].dice.buttonText = str(self.diceNumber)
                        if (self.tempTurn):
                            self.screenList[3][0].playerList[self.whoseTempTurn].posy += (34.5 * self.diceNumber)
                        else:
                            if self.direction is 0:
                                self.screenList[3][0].playerList[self.whoseTurn].posy -= (34.5 * self.diceNumber)
                            if self.direction is 1:
                                self.screenList[3][0].playerList[self.whoseTurn].posx += (80 * self.diceNumber)
                            if self.direction is 2:
                                self.screenList[3][0].playerList[self.whoseTurn].posy += (34.5 * self.diceNumber)
                            if self.direction is 3:
                                self.screenList[3][0].playerList[self.whoseTurn].posx -= (80 * self.diceNumber)
                        self.tempTurn = False

                        index = 0
                        for player in self.screenList[3][0].playerList:
                            if player is not self.screenList[3][0].playerList[self.whoseTurn]:
                                x1 = player.posx
                                x2 = self.screenList[3][0].playerList[self.whoseTurn].posx
                                y1 = player.posy
                                y2 = self.screenList[3][0].playerList[self.whoseTurn].posy
                                if (math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2) < 40):
                                    self.tempTurn = True
                                    self.whoseTempTurn = index
                            index += 1


                        self.whoseTurn = (self.whoseTurn+1)%self.nrPlayers


                    if self.screenList[3][0].direction:
                        self.direction = (self.direction+1)%4
                        if self.direction is 0:
                            self.screenList[3][0].direction.buttonText = "Up"
                        if self.direction is 1:
                            self.screenList[3][0].direction.buttonText = "Right"
                        if self.direction is 2:
                            self.screenList[3][0].direction.buttonText = "Down"
                        if self.direction is 3:
                            self.screenList[3][0].direction.buttonText = "Left"


                    self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]

        pygame.quit()
        sys.exit()

    def set_screen(self, width = 1280, height = 720):
        self.width = width
        self.height = height
        resolution = (width, height)
        self.screen = pygame.display.set_mode(resolution)


class Player():
    def __init__(self, screen, color, name, posx, posy):
        self.screen = screen
        self.color = color
        self.name = name
        self.posx = posx
        self.posy = posy
        self.sizex = 50
        self.sizey = 35

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.posx, self.posy, self.sizex,self.sizey))
        if self.posy < 0:
            print(self.name+" WON! posy= "+str(self.posy))




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
        for player in self.playerList:
            player.draw()
        self.dice.draw()
        self.direction.draw()

    def addButton(self, text, posx, posy, width = 600, height = 100):
        self.buttonList.append(MenuButton(self.screen, text, posx, posy, width, height))

    def addLabel(self, text, posx, posy, size = 50, color = (200, 200, 200)):
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))

    def addPlayer(self, color, name, posx, posy):
        self.playerList.append(Player(self.screen, color, name, posx, posy))

    def addDice(self, name, posx, posy, width = 100, height = 100):
        self.dice = MenuButton(self.screen, name, posx, posy, width, height)

    def addDirection(self, text, posx, posy, width = 100, height = 100):
        self.direction = MenuButton(self.screen, text, posx, posy, width, height)

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

    def addButton(self, text, posx, posy, width = 600, height = 100):
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
