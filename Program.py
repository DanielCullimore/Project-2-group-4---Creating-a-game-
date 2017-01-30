import pygame
import sys
from random import *
import math


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
        self.screenList =[] # List containing all screens

        # Init screens
        self.initScreens()


    def run(self):
        while not self.gameExit:
            # Display pygame screen
            for mainScreen in self.screenList:               # For all main screens
                for screen in mainScreen:                    # For all screens within main screens
                    if self.state is screen:                 # Filter out the pygame screen that should be active (the var self.state is changed through menu buttons)
                        screen.draw( *(self.passValues()) )  # Draw that screen, with var passed parameters

            pygame.display.flip()

            # Update pygame screen
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type is pygame.MOUSEBUTTONUP:
                    self.buttonFunctions()
                    if isinstance(self.state, playScreen):
                        self.dice(self.state)
                        self.directionFunction(self.state)
                    self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]
                if event.type is pygame.KEYUP:
                    if event.key == pygame.K_0:
                        self.state.whoseTurn = (self.state.whoseTurn + 1) % self.state.nrPlayers

        # Exit when self.gameExit
        pygame.quit()
        sys.exit()

    # Methods
    def set_screen(self, width = 1280, height = 720):
        self.width = width
        self.height = height
        resolution = (width, height)
        self.screen = pygame.display.set_mode(resolution)

    def initScreens(self):
        # Screens are in a grid
        # screen[0][0]
        # screen[1][0]  screen[1][1]    screen[1][2]
        # screen[2][0]
        # screen[3][0] screen[3][1]
        # etc.. So you can say screen = screen[currentScreen+1][0]
        # init main screen: Main Menu
        self.screenList.append([])  # Make room for new screen
        self.screenList[0].append(Menu(self.screen))  # Insert mainScreen (class object in list.)
        self.screenList[0][0].addButton("Play", (self.width / 2) - 300, 100)  # Add buttons to the screen
        self.screenList[0][0].addButton("Options", (self.width / 2) - 300, 250)
        self.screenList[0][0].addButton("Rules", (self.width / 2) - 300, 400)
        self.screenList[0][0].addButton("Exit", (self.width / 2) - 300, 550)
        # init subscreen: Options
        self.screenList[0].append(Menu(self.screen))  # insert subScreen (class object in list.)
        self.screenList[0][1].addButton("Back", (self.width / 2) - 300, 550)
        # init subscreen: Rules
        self.screenList[0].append(Menu(self.screen))
        self.screenList[0][2].addButton("Back", (self.width / 2) - 300, 550)

        # Init main screen: Choosing play-mode
        self.screenList.append([])  # Make room for new screen
        self.screenList[1].append(Menu(self.screen))
        self.screenList[1][0].addButton("Single Player", (self.width / 2) - 300, 100)
        self.screenList[1][0].addButton("Back", (self.width / 2) - 300, 250)

        # Init main screen: Single player play-mode settings screen
        self.screenList.append([])  # Make room for new screen
        self.screenList[2].append(Menu(self.screen))
        self.screenList[2][0].addButton("Play", (self.width / 2) - 300, 100)
        self.screenList[2][0].addLabel("Players = 4", (self.width / 2) - 600, 300)
        self.screenList[2][0].addButton("Back", 340, 450)

        # Init main screen: Actual playing board
        self.screenList.append([])  # Make room for new screen
        self.screenList[3].append(playScreen(self.screen))
        self.screenList[3][0].addBoard()
        self.screenList[3][0].addButton("Psuedo Play", -100, -100)
        self.screenList[3][0].addButton("Options", (self.width) - 255, 75, 270, 75)
        self.screenList[3][0].addButton("Psuedo Exit", -100, -100)
        self.screenList[3][0].addPlayer((255, 0, 0), "P1: Red Bob", 0, 11)
        self.screenList[3][0].addPlayer((0, 255, 0), "P2: Green Frank", 1, 11)
        self.screenList[3][0].addPlayer((0, 0, 255), "P3: Blue Mike", 6, 11)
        self.screenList[3][0].addPlayer((255, 0, 255), "P4: Magenta Fox", 7, 11)
        self.screenList[3][0].addDice("Dice", 50, 50)
        self.direction = 0
        self.screenList[3][0].addDirection("Direction", 150, 50)
        # Init subscreen: pauze game
        self.screenList[3].append(Menu(self.screen))
        self.screenList[3][1].addButton("Continue", (self.width / 2) - 300, 100)
        self.screenList[3][1].addButton("Main Menu", (self.width / 2) - 300, 550)

        # Init Win screen
        self.screenList.append([])  # Make room for new screen
        self.screenList[4].append(Menu(self.screen))


        # Init set screen to be active on default
        self.activeMainScreen = 0
        self.activeSubScreen = 0
        self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]

    def passValues(self):
        if isinstance(self.state, playScreen):
            return [self.state.whoseTurn, self.state.tempTurn, self.state.whoseTempTurn, self.state]
        else:
            return []

    def buttonFunctions(self):
        # Defining the action of button nr.1
        if (len(self.state.buttonList)) > 0:        # if more than 0 button
            if self.state.buttonList[0]:            #   if button is pressed
                if self.activeSubScreen > 0:        #       if a subscreen
                    self.activeSubScreen = 0        #           go back to its main screen
                else:                               #       else:
                    self.activeMainScreen += 1      #           go a main screen forward
                    self.activeSubScreen = 0
        # Defining the action of button nr.-1 (last)
        if (len(self.state.buttonList)) > 1:        # if more than 1 button
            if self.state.buttonList[-1]:           #   if last button is pressed
                if self.activeSubScreen == 0:       #       if not subscreen
                    if self.activeMainScreen == 0:  #           if screen[0][0]
                        self.gameExit = True        #               Exit
                    else:                           #           else:
                        self.activeMainScreen -= 1  #               screen -= 1
                        self.activeSubScreen = 0
                else:                               #       else (if subscreen, and last button pressed)
                    self.activeMainScreen = 0       #            go to main menu
                    self.activeSubScreen = 0
        # Defining the action of other buttons ("Take me to subscreen" buttons)
        if (len(self.state.buttonList) - 2) >= 0:  # if more than 2 buttons
            for i in range(len(self.state.buttonList) - 1):
                if self.state.buttonList[i]:
                    self.activeSubScreen = i

    def dice(self, state):
        self.whoseTurn = state.playerList[state.whoseTurn]
        self.whoseTempTurn = state.playerList[state.whoseTempTurn]

        if state.dice:
            self.diceNumber = randint(1, 6)
            state.dice.buttonText = str(self.diceNumber)
            if (state.tempTurn):
                print(1)
                self.whoseTempTurn.posY -= (1 * self.diceNumber)
            else:
                if self.direction is 0:
                    # TEST IF YOU REACH NEW AREA::
                    if (self.whoseTurn.posY <= 11) and (self.whoseTurn.posY + self.diceNumber > 11):
                        if self.whoseTurn.posX is 0 or self.whoseTurn.posX is 1:
                            self.whoseTurn.posX = 2
                            print("P1")
                        elif self.whoseTurn.posX is 6 or self.whoseTurn.posX is 7:
                            self.whoseTurn.posX = 5
                            print("P4")
                        elif self.whoseTurn.posX is 2 or self.whoseTurn.posX is 3:
                            self.whoseTurn.posX = 3
                            print("P2")
                        elif self.whoseTurn.posX is 4 or self.whoseTurn.posX is 5:
                            self.whoseTurn.posX = 4
                            print("P3")
                        #self.screenList[3][0].playerList[state.whoseTurn].posX = int((self.screenList[3][0].playerList[state.whoseTurn].posX % 4) + 1)
                    self.whoseTurn.posY += (1 * self.diceNumber)
                if self.direction is 1:
                    self.whoseTurn.posX += (1 * self.diceNumber)
                if self.direction is 2:
                    self.whoseTurn.posY -= (1 * self.diceNumber)
                if self.direction is 3:
                    self.whoseTurn.posX -= (1 * self.diceNumber)



    def directionFunction(self, state):
        if state.direction:
            self.direction = (self.direction + 1) % 4
            if self.direction is 0:
                state.direction.buttonText = "Up"
            if self.direction is 1:
                state.direction.buttonText = "Right"
            if self.direction is 2:
                state.direction.buttonText = "Down"
            if self.direction is 3:
                state.direction.buttonText = "Left"

class Player():
    def __init__(self, screen, color, name, posx, posy):
        self.screen = screen
        self.color = color
        self.name = name
        self.posX = posx
        self.posY = posy
        self.sizeX = 50
        self.sizeY = 35

    def moveAlongBoard(self):
        # Finish Line
        if self.posY >= 17:
            self.posY = 17
            print(self.name + " WON!")

        # Last 5 steps
        if self.posY >= 12 and (self.posX > 5 or self.posX < 2):
            self.posX = (self.posX+2) % 4 + 2


        if self.posX > 7 or self.posX < 0:
            self.posX = self.posX % 8 + 1
        if self.posY < 0:
            self.posY = 0

    def checkOverlap(self, state):
        state.tempTurn = False
        #index = 0
        for player in state.playerList:
            if player is not state.playerList[state.whoseTurn]: #For all other players in playerList
                x1 = player.posX #other player pos
                x2 = state.playerList[state.whoseTurn].posX #whoseturn player pos
                y1 = player.posY
                y2 = state.playerList[state.whoseTurn].posY
                if (x1 is x2) and (y1 is y2):  # "Ouch! You hit me! "
                    state.tempTurn = True
                    state.whoseTempTurn = state.playerList.index(player)  # p0, p1, p3 or p4
                    print("whoseTurn = "+str(state.whoseTurn))
                    print("TempTurn = "+str(state.whoseTempTurn))
                    break
                    # self.whoseTurn -= 1
            #print(index)
            #index += 1

    def draw(self, state): # State == screen
        if state.whoseTurn is state.playerList.index(self):
            self.moveAlongBoard()
            self.checkOverlap(state)

        pygame.draw.rect(self.screen, self.color, (state.board.grid[self.posX + self.posY*8].posX +8,
                                                   state.board.grid[self.posX + self.posY*8].posY +2,
                                                   self.sizeX,self.sizeY))


class box:
    def __init__(self, screen, boxPosX, boxPosY, boxSizeX, boxSizeY, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.boxSizeX = boxSizeX
        self.boxSizeY = boxSizeY
        self.boxPosX = boxPosX
        self.boxPosY = boxPosY
        self.sizeY = self.boxSizeY / 19
        self.sizeX = self.boxSizeX/ 8
        self.posX = self.boxPosX+(self.x*self.sizeX)
        self.posY = self.boxPosY+self.boxSizeY-(self.y*self.sizeY)-self.sizeY
        self.category = 0
        self.color = (0,0,0)
        self.font = pygame.font.SysFont('moonspace', 12)

        #print(self.boxSizeY)
        if (self.y is 18 or self.y is 17) and self.x > 1 and self.x < 6:
            self.category = 5 #FINISH
        else:
            if self.y > 11:
                if self.x is 2:
                    self.category = 1 # Red
                elif self.x is 3:
                    self.category = 2  # Green
                elif self.x is 4:
                    self.category = 3
                elif self.x is 5:
                    self.category = 4
            else:
                if self.x is 1 or x is 0:
                    self.category = 1 # Red
                elif self.x is 2 or x is 3:
                    self.category = 2 # Green
                elif self.x is 4 or self.x is 5:
                    self.category = 3
                elif self.x is 6 or self.x is 7:
                    self.category = 4

        if self.category is 1:
            self.color = (67,87,114)
        elif self.category is 2:
            self.color = (254,170,58)
        elif self.category is 3:
            self.color = (253,96,65)
        elif self.category is 4:
            self.color = (177,207,55)
        elif self.category is 5:
            self.color = (125,125,125)

        if self.y is 0 or self.y is 1:
            red, green, blue = self.color
            self.color = (125,125,125)


    def draw(self):
        pygame.draw.rect(self.screen, self.color, ( self.posX,
                                                    self.posY,
                                                    self.sizeX,
                                                    self.sizeY,))
        if (self.y is not 0 and self.y is not 1 and self.y is not 17 and self.y is not 18):
            pygame.draw.rect(self.screen, (0,0,0), (self.posX,
                                                       self.posY,
                                                       self.sizeX,
                                                       self.sizeY,), 2)


        screen_text = self.font.render("x="+str(self.x)+"  y="+str(self.y), True, (255,255,255))
        self.screen.blit(screen_text, (self.posX+self.sizeX/4, self.posY+self.sizeY/4))
        #pygame.display.update()

class playBoard:
    def __init__(self, screen):
        self.screen = screen
        width, height = self.screen.get_size()
        self.sizeY = height*0.9
        self.sizeX = self.sizeY/19*8*2
        self.posX = width/2-(self.sizeX/2)
        self.posY = (height-self.sizeY)/2

        self.grid = []

        for y in range(19):
            for x in range(8):
                self.grid.append(box(self.screen, self.posX, self.posY ,self.sizeX, self.sizeY, x,y))

    def draw(self):
        #pygame.draw.rect(self.screen, (150,150,150), (self.posX,self.posY,self.sizeX,self.sizeY))
        for box in self.grid:
            box.draw()


class playScreen:
    def __init__(self, screen):
        self.screen = screen
        #self.background = pygame.image.load("res/spelbord.jpg")
        #self.backgroundtransformed = pygame.transform.scale(self.background, (int(1280 * 0.5), int(720) - 200))
        self.buttonList = []
        self.labelList = []
        self.playerList = []
        self.actionList = []
        self.board = 0
        self.font = pygame.font.SysFont('moonspace', 30)

        #
        self.whoseTurn = 0
        self.nrPlayers = 4

        # Init special action
        self.tempTurn = False
        self.whoseTempTurn = 0



    def draw(self, whoseTurn, tempTurn, whoseTempTurn, state):
        self.screen.fill((0, 0, 0))
        #self.screen.blit(self.backgroundtransformed, (1280 / 4, 100))

        self.board.draw()

        for button in self.buttonList:
            button.draw()
        for label in self.labelList:
            label.draw()
        for player in self.playerList:
            player.draw(state)
        #self.checkOverlap(state)
        self.dice.draw()
        self.direction.draw()
        if tempTurn:
            self.players_turn("Player " + str(self.playerList[whoseTempTurn].name) + " has to move backwards! Roll the dice", (255, 255, 255))
        else:
            self.players_turn("Player "+str(self.playerList[whoseTurn].name)+" turn", (255, 255, 255))

    def addBoard(self):
        self.board = playBoard(self.screen)

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

    def players_turn(self, msg, color):
        screen_text = self.font.render(msg, True, color)
        self.screen.blit(screen_text, (10, 575))
        pygame.display.update()

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
        #self.font = pygame.font.SysFont('moonspace', 10)
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
