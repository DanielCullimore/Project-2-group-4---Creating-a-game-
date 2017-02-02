import pygame
import sys
from random import *
import math
import configparser
import database as db

class Game:

    def __init__(self):
        # Init pygame
        pygame.init()
        pygame.font.init()

        self.p = Properties()
        self.set_screen()

        self.set_screen()
        self.fps = 60
        self.gameExit = False
        self.clock = pygame.time.Clock()

        # Init game
        self.screenList =[] # List containing all screens

        # Init screens
        self.initScreens()
        self.state = self.screenList[0][0]

        #
        self.nrPlayers = 4
        self.completed = False


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
            pygame.display.set_caption("Project 2 - FPS: " + str(int(self.clock.get_fps())))

            if self.completed:
                self.activeMainScreen = -1
                #print("OVER!!!!!!!!!!!!!!!!!!!")

            for event in pygame.event.get():
                if event.type is pygame.VIDEORESIZE:
                    tempMain = self.activeMainScreen
                    tempSub = self.activeSubScreen
                    self.screenList.clear()
                    if event.h < 480 or event.w < 640:
                        self.p.set("width", "1024")
                        self.p.set("height", "768")
                    else:
                        self.p.set("width", str(event.w))
                        self.p.set("height", str(event.h))

                    self.set_screen()
                    self.initScreens()

                    self.activeMainScreen = tempMain
                    self.activeSubscreen = tempSub
                    self.state = self.screenList[tempMain][tempSub]


                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type is pygame.MOUSEBUTTONUP:
                    self.buttonFunctions()
                    if isinstance(self.state, playScreen):
                        self.dice(self.state)
                        self.directionFunction(self.state)
                    self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]
                if event.type is pygame.KEYUP:
                    if event.key == pygame.K_0 and self.state.roundNr is 1:
                        self.state.whoseTurn = (self.state.whoseTurn + 1) % self.state.nrPlayers
                        if self.state.whoseTurn is 0:
                            self.state.roundNr += 1
            if isinstance(self.state, playScreen):
                for player in self.state.playerList:
                    if player.imdone:
                        player.imdone = False
                        self.state.whoseTurn = (self.state.whoseTurn + 1) % self.state.nrPlayers
                        if self.state.whoseTurn is 0:
                            self.state.roundNr += 1






        # Exit when self.gameExit
        pygame.quit()
        sys.exit()

    def set_screen(self):
        flags = pygame.HWSURFACE
        width = self.p.get("width", "int")
        height = self.p.get("height", "int")
        if self.p.get("doublebuffering", "bool"):
            flags |= pygame.DOUBLEBUF
        if self.p.get("fullscreen", "bool"):
            flags |= pygame.FULLSCREEN
        if self.p.get("resizable", "bool"):
            flags |= pygame.RESIZABLE
        self.screen = pygame.display.set_mode((width, height), flags)
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()

    # Methods
    # def set_screen(self, width = 1280, height = 720):
    #     self.width = width
    #     self.height = height
    #     resolution = (width, height)
    #     self.screen = pygame.display.set_mode(resolution)

    def initScreens(self):
        # Screens are in a grid
        # screen[0][0]
        # screen[1][0]  screen[1][1]    screen[1][2]
        # screen[2][0]
        # screen[3][0] screen[3][1]
        # etc.. So you can say screen = screen[currentScreen+1][0]
        # init main screen: Main Menu
        self.screenList.append([])  # Make room for new screen
        self.screenList[0].append(Menu(self.p))  # Insert mainScreen (class object in list.)
        self.screenList[0][0].addButton("Play", int(self.width / 3.75), 100)  # Add buttons to the screen
        self.screenList[0][0].addButton("Options", int(self.width / 3.75), 220)
        self.screenList[0][0].addButton("Rules", int(self.width / 3.75), 340)
        self.screenList[0][0].addButton("Highscore", int(self.width / 3.75), 460)
        self.screenList[0][0].addButton("Exit", int(self.width / 3.75), 580)
        # init subscreen: Options
        self.screenList[0].append(Menu(self.p))  # insert subScreen (class object in list.)
        #self.screenList[0][1].addButton("Back", int(self.width / 3.75), 550)

        self.screenList[0][1].addLabel("Fullscreen: ", int(self.width / 10 * 4), int(self.height / 10 * 1),size=int(self.height / 36))
        self.screenList[0][1].addCheckbox("fullscreen", int(self.width / 10 * 6), int(self.height / 10 * 1))
        self.screenList[0][1].addLabel("DoubleBuffering: ", int(self.width / 10 * 4), int(self.height / 10 * 2),size=int(self.height / 36))
        self.screenList[0][1].addCheckbox("doublebuffering", int(self.width / 10 * 6), int(self.height / 10 * 2))
        self.screenList[0][1].addLabel("Resizable: ", int(self.width / 10 * 4), int(self.height / 10 * 3),size=int(self.height / 36))
        self.screenList[0][1].addCheckbox("resizable", int(self.width / 10 * 6), int(self.height / 10 * 3))
        self.screenList[0][1].addButton("Back", int(self.width / 3.75), int(self.height / 10 * 7))

        # init subscreen: Rules
        self.screenList[0].append(Menu(self.p))
        self.screenList[0][2].addLabel1("The game is played with 2 - 4 players.", (self.width / 2) - 625, 20)
        self.screenList[0][2].addLabel1("There is a dice you can roll when you", (self.width / 2) - 625, 55)
        self.screenList[0][2].addLabel1("answer a question correctly.", (self.width / 2) - 625, 90)
        self.screenList[0][2].addLabel1("If a player ends up on another players hole, the player who",
                                        (self.width / 2) - 625, 150)
        self.screenList[0][2].addLabel1("was already on that hole throws a dice", (self.width / 2) - 625, 185)
        self.screenList[0][2].addLabel1("The number given after throwing the dice (numbers 1 to 6)",
                                        (self.width / 2) - 625, 220)
        self.screenList[0][2].addLabel1("is the number the player has to go down", (self.width / 2) - 625, 255)
        self.screenList[0][2].addLabel1("There are four different categories, each with its own color",
                                        (self.width / 2) - 625, 325)
        self.screenList[0][2].addLabel1("and questions: Blue = Sports, Green = Geography,", (self.width / 2) - 625, 360)
        self.screenList[0][2].addLabel1("Red = Entertainment and Yellow = History", (self.width / 2) - 625, 395)
        self.screenList[0][2].addButton("Back", int(self.width / 3.75), 550)


        self.screenList[0].append(Menu(self.p))  # Insert mainScreen#  (class object in list.)
        self.screenList[0][3].addLabel("Highscores", int(self.width / 2.75), 50)

        self.screenList[0][3].addLabel("First place: {} {}".format(str(scores.Firstname), str(scores.Firstscore)),
                                       int(self.width / 2.5), 200, size=20)
        self.screenList[0][3].addLabel("Second place: {} {} ".format(str(scores.Secondname), str(scores.Secondscore)),
                                       int(self.width / 2.5), 300, size=20)
        self.screenList[0][3].addLabel("Third place: {} {}".format(str(scores.Thirdname), str(scores.Thirdscore)),
                                       int(self.width / 2.5), 400, size=20)
        self.screenList[0][3].addButton("Back", int(self.width / 2.75), 500)  # Add buttons to the screen

        # Init main screen: Choosing play-mode
        self.screenList.append([])  # Make room for new screen
        self.screenList[1].append(Menu(self.p))
        self.screenList[1][0].addButton("Single Player", int(self.width / 3.75), 100)
        self.screenList[1][0].addButton("Back", int(self.width / 3.75), 250)

        # Init main screen: Single player play-mode settings screen
        self.screenList.append([])  # Make room for new screen
        self.screenList[2].append(Menu(self.p))
        self.screenList[2][0].addButton("Play", int(self.width / 3.75), 100)
        self.screenList[2][0].addLabel("Players = ", int(self.width / 3.75) - 300, 300)
        self.screenList[2][0].addPlayerButton("4", int(self.width/3.75) - 50, 280)
        self.screenList[2][0].addButton("Back", 340, 450)

        # Init main screen: Actual playing board
        self.screenList.append([])  # Make room for new screen
        self.screenList[3].append(playScreen(self.p))
        self.screenList[3][0].addBoard()
        self.screenList[3][0].addButton("Psuedo Play", -100, -100)
        self.screenList[3][0].addButton("Options", int(self.width) - 255, 75, 270, 75)
        self.screenList[3][0].addButton("Psuedo Exit", -100, -100)
        self.screenList[3][0].addPlayer((255, 0, 0), "P1: Red Bob", 0, 0, "res/Player red.png", self.screenList[3][0])
        self.screenList[3][0].addPlayer((0, 255, 0), "P2: Green Frank", 2, 0, "res/Player green.png", self.screenList[3][0])
        self.screenList[3][0].addPlayer((0, 0, 255), "P3: Blue Mike", 4, 0, "res/Player blue.png", self.screenList[3][0])
        self.screenList[3][0].addPlayer((255, 0, 255), "P4: Magenta Fox", 6, 0, "res/Player yellow.png", self.screenList[3][0])
        self.screenList[3][0].addDice("Dice", 50, 50)
        self.direction = 0
        self.screenList[3][0].addDirection("Direction", 150, 50)
        # Init subscreen: pauze game
        self.screenList[3].append(Menu(self.p))
        self.screenList[3][1].addButton("Continue", int(self.width / 3.75), 100)
        self.screenList[3][1].addButton("PSUEDO", int(self.width+10), 0)
        self.screenList[3][1].addButton("Read rules", int(self.width / 3.75) + 200, 300)
        self.screenList[3][1].addButton("Main Menu", int(self.width / 3.75), 550)
        self.screenList[3][1].addLabel("Players = ", int(self.width / 3.75) -300, 300)
        self.screenList[3][1].addPlayerButton("4", int(self.width / 3.75)-50, 280)
        # Init subscreen: Rules
        self.screenList[3].append(Menu(self.p))
        self.screenList[3][2].addLabel1("The game is played with 2 - 4 players.", (self.width / 2) - 625, 20)
        self.screenList[3][2].addLabel1("There is a dice you can roll when you", (self.width / 2) - 625, 55)
        self.screenList[3][2].addLabel1("answer a question correctly.", (self.width / 2) - 625, 90)
        self.screenList[3][2].addLabel1("If a player ends up on another players hole, the player who",
                                        (self.width / 2) - 625, 150)
        self.screenList[3][2].addLabel1("was already on that hole throws a dice", (self.width / 2) - 625, 185)
        self.screenList[3][2].addLabel1("The number given after throwing the dice (numbers 1 to 6)",
                                        (self.width / 2) - 625, 220)
        self.screenList[3][2].addLabel1("is the number the player has to go down", (self.width / 2) - 625, 255)
        self.screenList[3][2].addLabel1("There are four different categories, each with its own color",
                                        (self.width / 2) - 625, 325)
        self.screenList[3][2].addLabel1("and questions: Blue = Sports, Green = Geography,", (self.width / 2) - 625, 360)
        self.screenList[3][2].addLabel1("Red = Entertainment and Yellow = History", (self.width / 2) - 625, 395)
        self.screenList[3][2].addButton("Back", int(self.width / 3.75), 550)

        # Init Win screen
        self.screenList.append([])  # Make room for new screen
        self.screenList[4].append(Menu(self.p))
        self.screenList[4][0].addLabel("You Won!", int(self.width/3.75), 100)

        # Init set screen to be active on default
        self.activeMainScreen = 0
        self.activeSubScreen = 0
        #self.state = self.screenList[self.activeMainScreen][self.activeSubScreen]

    def passValues(self):
        if isinstance(self.state, playScreen):
            return [self.state.whoseTurn, self.state.tempTurn, self.state.whoseTempTurn, self.state, self.state.roundNr, self.activeMainScreen, self.nrPlayers]
        else:
            return []

    def buttonFunctions(self):
        if self.state is self.screenList[0][1]:
            if self.state.buttonList[0]:
                self.state = self.screenList[0][0]
            elif self.state.checkboxList[0] and not self.state.checkboxList[2].isChecked:
                if self.state.checkboxList[0].isChecked:
                    self.screenList.clear()
                    self.p.set("fullscreen", "False")
                    self.p.set("width", "1280")
                    self.p.set("height", "720")
                    self.set_screen()
                    self.initScreens()
                    self.state = self.screenList[0][1]
                    self.activeMainScreen = 0
                    self.activeSubScreen = 1
                    self.state.checkboxList[0].isChecked = False
                else:
                    self.screenList.clear()
                    self.p.set("fullscreen", "True")
                    self.p.set("width", "1920")
                    self.p.set("height", "1080")
                    self.set_screen()
                    self.initScreens()
                    self.state = self.screenList[0][1]
                    self.activeMainScreen = 0
                    self.activeSubScreen = 1
                    self.state.checkboxList[0].isChecked = True
            elif self.state.checkboxList[1]:
                if self.state.checkboxList[1].isChecked:
                    self.screenList.clear()
                    self.p.set("doublebuffering", "False")
                    self.set_screen()
                    self.initScreens()
                    self.state = self.screenList[0][1]
                    self.activeMainScreen = 0
                    self.activeSubScreen = 1
                    self.state.checkboxList[1].isChecked = False
                else:
                    self.screenList.clear()
                    self.p.set("doublebuffering", "True")
                    self.set_screen()
                    self.initScreens()
                    self.state = self.screenList[0][1]
                    self.activeMainScreen = 0
                    self.activeSubScreen = 1
                    self.state.checkboxList[1].isChecked = True
            elif self.state.checkboxList[2] and not self.state.checkboxList[0].isChecked:
                if self.state.checkboxList[2].isChecked:
                    self.screenList.clear()
                    self.p.set("resizable", "False")
                    self.set_screen()
                    self.initScreens()
                    self.state = self.screenList[0][1]
                    self.activeMainScreen = 0
                    self.activeSubScreen = 1
                    self.state.checkboxList[2].isChecked = False
                else:
                    self.screenList.clear()
                    self.p.set("resizable", "True")
                    self.set_screen()
                    self.initScreens()
                    self.state = self.screenList[0][1]
                    self.activeMainScreen = 0
                    self.activeSubScreen = 1
                    self.state.checkboxList[2].isChecked = True
            if self.state.buttonList[-1]:
                self.activeMainScreen = 0
                self.activeSubScreen = 0
        else:
            #print(11)
            # Defining the action of button nr.1
            if (len(self.state.buttonList)) > 0:        # if more than 0 button (prevent list index out of range)
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

            ###Action button
            if len(self.state.actionList) > 0:
                if self.state.actionList[0]:
                    self.nrPlayers = (self.nrPlayers % 4) +1
                    self.state.actionList[0].buttonText = str(self.nrPlayers)



    def dice(self, state):
        self.whoseTurn = state.playerList[state.whoseTurn]
        self.whoseTempTurn = state.playerList[state.whoseTempTurn]

        if state.dice and state.roundNr > 1:

            self.diceNumber = randint(1, 6)
            self.moveNumber = math.ceil(self.diceNumber/2)
            state.dice.buttonText = str(self.diceNumber)

            if not self.state.tempTurn:
                x = QuestionScreen(self.screen, self.p, self.whoseTurn).run()
            else:
                x = True
            if x or self.state.tempTurn:
                if (state.tempTurn):
                    self.whoseTempTurn.moving = True
                    self.whoseTempTurn.steps = 0
                    #print(1)
                    self.whoseTempTurn.moveToPosY -= (1 * self.moveNumber)
                    if self.whoseTempTurn.moveToPosY <= 0:
                        self.whoseTempTurn.moveToPosY = 0
                else:
                    self.whoseTurn.moving = True
                    self.whoseTurn.steps = 0
                    if self.direction is 0:
                        # TEST IF YOU REACH NEW AREA::
                        if (self.whoseTurn.posY <= 11) and (self.whoseTurn.posY + self.moveNumber > 11):
                            if self.whoseTurn.posX is 0 or self.whoseTurn.posX is 1:
                                self.whoseTurn.moveToPosX = 2
                                print("P1")
                            elif self.whoseTurn.posX is 6 or self.whoseTurn.posX is 7:
                                self.whoseTurn.moveToPosX = 5
                                print("P4")
                            elif self.whoseTurn.posX is 2 or self.whoseTurn.posX is 3:
                                self.whoseTurn.moveToPosX = 3
                                print("P2")
                            elif self.whoseTurn.posX is 4 or self.whoseTurn.posX is 5:
                                self.whoseTurn.moveToPosX = 4
                                print("P3")
                            #self.screenList[3][0].playerList[state.whoseTurn].posX = int((self.screenList[3][0].playerList[state.whoseTurn].posX % 4) + 1)
                        self.whoseTurn.moveToPosY += (1 * self.moveNumber)
                    if self.direction is 1:
                        self.whoseTurn.moveToPosX += (1 * self.moveNumber)
                    if self.direction is 2:
                        self.whoseTurn.moveToPosY -= (1 * self.moveNumber)
                    if self.direction is 3:
                        self.whoseTurn.moveToPosX -= (1 * self.moveNumber)

                self.whoseTurn.moveAlongBoard(state)

                if self.whoseTurn.moveToPosY >= 17:
                    print("Player "+str(self.whoseTurn.name)+" won the game!")
                    self.completed = True
                    self.screenList[4][0].labelList[0].text = "Player "+str(self.whoseTurn.name)+" won the game!"
                    db.upload_score(str(self.whoseTurn.name), state.roundNr)
                    ## self.activemainscreen += 1
            else:
                self.whoseTurn.imdone = True


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

class Properties:
    def __init__(self):
        self.filepath = "properties.cfg"  # default file path (same directory as Program.py)
        self.section = "PROPERTIES"
        self.config = configparser.ConfigParser()
        self.config.sections()
        try:
            with open(self.filepath) as f:
                self.config.read_file(f)
        except IOError:
            self._init_default()  # if file does not exist, it creates new default properties.cfg file

    def get(self, prop, type=None):  # Prop = property
        if type is None:
            return self.config.get(self.section, prop)
        elif type is "int":
            return self.config.getint(self.section, prop)
        elif type is "bool":
            return self.config.getboolean(self.section, prop)
        elif type is "float":
            return self.config.getfloat(self.section, prop)

    def set(self, prop, value):  # this method also has the ability to create new properties
        self.config.set(self.section, prop, value)
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)

    def _init_default(self):
        self.config[self.section] = {"width": 1280,
                                     "height": 720,
                                     "resizable": False,
                                     "doublebuffering": False,
                                     "fullscreen": False}
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, color, name, posx, posy, skinPath, state):
        self.screen = screen
        self.color = color
        self.name = name

        self.imdone = False

        # Sprite
        pygame.sprite.Sprite.__init__(self)
        self.ss = Spritesheet(skinPath, 5, 4, (200, 200))
        self.playerSpeed = 4.0
        self.image = self.ss.get_sprite(0, 0)  # Holds the actual surface object
        self.frame = 1  # holds the frame index which is to be drawn.
        self.threshold = 0  # holds the number of times the image will be drawn before switching frame.
        self.lastState = 0
        self.rect = self.image.get_rect()

        ### MOVE TOWARDS POSITION
        self.posX = posx #is the position of the player
        self.posY = posy

        self.moving = False #Is True after dice is thrown, until new position is being reached
        self.steps = 0
        self.moveToPosX = self.posX
        self.moveToPosY = self.posY

        self.posXOnScreen = state.board.grid[self.posX + self.posY * 8].posX + 11
        self.posYOnScreen = state.board.grid[self.posX + self.posY * 8].posY - 20
        self.moveToPosXOnScreen = 0
        self.moveToPosYOnScreen = 0

        self.moveX = 0
        self.moveY = 0

        self.sizeX = 50
        self.sizeY = 35

    def moveAlongBoard(self, state):
        #print("Moving along board..........")
        # Finish Line
        if self.moveToPosY >= 17:
            self.moveToPosY = 17
            print(self.name + " WON!")


        # Last 5 steps
        if self.moveToPosY >= 12 and (self.moveToPosX > 5 or self.moveToPosX < 2):
            self.moveToPosX = (self.moveToPosX+2) % 4 + 2
        if self.moveToPosX > 7 or self.moveToPosX < 0:
            self.moveToPosX = (self.moveToPosX) % 8
            #print("shoo")
        if self.moveToPosY < 0:
            self.moveToPosY = 0

    def move(self, state):
        if self.moving:
            self.steps += 1

            #print("Player " + str(state.playerList[state.whoseTurn].name) + " is moving")
            if self.steps is 1:
                self.moveToPosXOnScreen = state.board.grid[self.moveToPosX + self.moveToPosY * 8].posX + 11
                self.moveToPosYOnScreen = state.board.grid[self.moveToPosX + self.moveToPosY * 8].posY - 20
                self.moveX = (self.moveToPosXOnScreen-self.posXOnScreen)/40
                self.moveY = (self.moveToPosYOnScreen-self.posYOnScreen)/40
                #self.playerSpeed = self.moveY+2
            #print(self.moveX)
            self.posXOnScreen += self.moveX
            self.posYOnScreen += self.moveY

            if self.steps > 40:
                self.moving = False
                self.posX = self.moveToPosX
                self.posY = self.moveToPosY
                #print("I'm no longer moving")
                self.checkOverlap(state)

                self.imdone = True




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
                    break


    def drawMoveableSprite(self, state):
        #
        #print(str(state.playerList[state.whoseTurn].name))
        self.rect = self.screen.blit(self.image, (self.posXOnScreen, self.posYOnScreen))
        self.threshold += 1
        if self.threshold is 8:
            self.threshold = 0
            if self.frame is self.ss.maxColumns - 1:
                self.frame = 1
            else:
                self.frame += 1
        if True: #insert whoseturn here
            if pygame.key.get_pressed()[pygame.K_UP] and self.posY >= 0:
                self.image = self.ss.get_sprite(self.frame, 2)
                self.posYOnScreen -= self.playerSpeed
                self.lastState = 2
            elif pygame.key.get_pressed()[pygame.K_DOWN] and self.posY <= 18:
                self.image = self.ss.get_sprite(self.frame, 0)
                self.posYOnScreen += self.playerSpeed
                self.lastState = 0
            elif pygame.key.get_pressed()[pygame.K_LEFT] and self.posX >= 0:
                self.image = self.ss.get_sprite(self.frame, 3)
                self.posXOnScreen -= self.playerSpeed
                self.lastState = 3
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and self.posX <= 8:
                self.image = self.ss.get_sprite(self.frame, 1)
                self.posXOnScreen += self.playerSpeed
                self.lastState = 1
            else:
                self.image = self.ss.get_sprite(0, self.lastState)


        self.posY = 1
        self.moveToPosX = self.posX
        self.moveToPosY = self.posY



    def drawMoving(self, state):
        #self.posYOnScreen = state.board.grid[self.posX + self.posY * 8].posY - 20
        #self.playerSpeed = 1
        self.rect = self.screen.blit(self.image, (self.posXOnScreen, self.posYOnScreen))
        self.threshold += 1
        # pygame.draw.rect(self.screen, self.color, (self.posXOnScreen,
        #                                            self.posYOnScreen,
        #                                            self.sizeX, self.sizeY))
        if self.threshold is 8:
            self.threshold = 0
            if self.frame is self.ss.maxColumns - 1:
                self.frame = 1
            else:
                self.frame += 1

        if (self.moveToPosY > self.posY):  # GO UP
            self.image = self.ss.get_sprite(self.frame, 2)
            self.lastState = 2
            #print("WIJASJDIASD")
        elif (self.moveToPosY < self.posY): # Move down
            self.image = self.ss.get_sprite(self.frame, 0)
            self.lastState = 0
        elif (self.moveToPosX > self.posX): # RIGHT
            self.image = self.ss.get_sprite(self.frame, 1)
            self.lastState = 1
        elif (self.moveToPosX < self.posX): # LEFT
            self.image = self.ss.get_sprite(self.frame, 3)
            self.lastState = 3


    def drawStatic(self, state):
        if state.roundNr is 1:
            if self.posXOnScreen < state.board.posX:
                self.posX = 0
            elif self.posXOnScreen > state.board.posX+state.board.sizeX:
                self.posX = 7

        #update posX
        self.posX = int(((self.posXOnScreen - state.board.posX) / (state.board.sizeX/8)))%8
        self.moveToPosX = self.posX
        self.moveToPosY = self.posY

        self.posXOnScreen = state.board.grid[self.posX + self.posY * 8].posX + 11
        self.posYOnScreen = state.board.grid[self.posX + self.posY * 8].posY - 20

        self.rect = self.screen.blit(self.image, (self.posXOnScreen, self.posYOnScreen))

        self.threshold = 0
        self.image = self.ss.get_sprite(0, self.lastState)


    def draw(self, state): # State == screen

        self.category = state.board.grid[self.posX + self.posY * 8].category
        if self.category is 1:
            self.category = "Sport"
        elif self.category is 2:
            self.category = "Historie" #taal faal
        elif self.category is 3:
            self.category = "Entertainment"
        elif self.category is 4:
            self.category = "Geografie"
        # if state.playerList[state.whoseTurn].name is self.name:
        #     print("Player " + str(state.playerList[state.whoseTurn].name) + " category = "+str(self.category))

        if (state.whoseTurn is state.playerList.index(self) or (state.tempTurn and state.whoseTempTurn is state.playerList.index(self))):
            if self.moving:
                self.move(state)
                self.drawMoving(state)
            elif state.roundNr is 1:
                self.drawMoveableSprite(state)
            else:
                self.posYOnScreen = state.board.grid[self.posX + self.posY * 8].posY - 20
                self.drawStatic(state)
        else:
            self.drawStatic(state)

class Spritesheet:  # a container for holding the image

    def __init__(self, filePath, maxColumns, maxRows, scale=None, colorkey = (255, 255, 255)):
        self.colorkey = colorkey
        self.stripes = []  # holds the tuples which contain four vectors to form a rectangle
        self.spritesheet = pygame.image.load(filePath).convert()
        self.maxColumns = maxColumns
        self.maxRows = maxRows
        if scale is not None:
            self.scale(scale)
        else:
            self.sheetSize = self.spritesheet.get_size()
            self.spriteWidth = int(self.sheetSize[0]/maxColumns)
            self.spriteHeight = int(self.sheetSize[1]/maxRows)
        self.init_sprites()

    def scale(self, scale):
        self.spritesheet = pygame.transform.scale(self.spritesheet, scale)
        self.sheetSize = self.spritesheet.get_size()
        self.spriteWidth = int(self.sheetSize[0]/self.maxColumns)
        self.spriteHeight = int(self.sheetSize[1]/self.maxRows)

    def init_sprites(self):
        posx = [x for x in range(0, self.sheetSize[0], self.spriteWidth)]
        posy = [y for y in range(0, self.sheetSize[1], self.spriteHeight)]
        self.stripes = []
        for i in range(0, self.maxRows):
            self.stripes.append([])
            for j in range(0, self.maxColumns):
                self.stripes[i].append((posx[j], posy[i], self.spriteWidth, self.spriteHeight))

    def get_sprite(self, column, row):
        rect = pygame.Rect(self.stripes[row][column])
        cropped = pygame.Surface((self.spriteWidth, self.spriteHeight))
        cropped.blit(self.spritesheet, (0, 0), rect)
        cropped.set_colorkey(self.colorkey)
        return cropped

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
        self.color = (0,0,0,0)
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


        #screen_text = self.font.render("x="+str(self.x)+"  y="+str(self.y), True, (255,255,255))
        #self.screen.blit(screen_text, (self.posX+self.sizeX/4, self.posY+self.sizeY/4))
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
    def __init__(self, p):
        self.p = p
        #width, height = self.screen.get_size()
        self.set_screen()
        self.background = pygame.image.load("res/bg.jpg")
        self.backgroundtransformed = pygame.transform.scale(self.background, (self.width, self.height))
        self.buttonList = []
        self.labelList = []
        self.playerList = []
        self.actionList = []
        self.board = 0
        self.font = pygame.font.SysFont('moonspace', 30)

        #
        self.whoseTurn = 0
        self.roundNr = 1
        self.nrPlayers = 4

        # Init special action
        self.tempTurn = False
        self.whoseTempTurn = 0


    def set_screen(self):
        flags = 0x0
        width = self.p.get("width", "int")
        height = self.p.get("height", "int")
        if self.p.get("doublebuffering", "bool"):
            flags |= pygame.DOUBLEBUF
        if self.p.get("fullscreen", "bool"):
            flags |= pygame.FULLSCREEN
        if self.p.get("resizable", "bool"):
            flags |= pygame.RESIZABLE
        self.screen = pygame.display.set_mode((width, height), flags)
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()

    def draw(self, whoseTurn, tempTurn, whoseTempTurn, state, roundNr, activeMainScreen, nrPlayers):
        self.nrPlayers = nrPlayers
        #self.screen.fill((0, 0, 0))
        self.screen.blit(self.backgroundtransformed, (0, 0))

        self.board.draw()

        for button in self.buttonList:
            button.draw()
        for label in self.labelList:
            label.draw()
        for player in self.playerList[0:self.nrPlayers]:
            player.draw(state)
        #self.checkOverlap(state)
        self.dice.draw()
        self.direction.draw()
        self.round("Round "+str(self.roundNr), (0,0,0))
        if self.roundNr is 1:
            self.explain("Move your character to","the desired category","If you're ready press 0", (0,0,0))
        elif self.roundNr is 2:
            self.explain("Throw the dice!", "","", (0, 0, 0))
        if tempTurn:
            self.players_turn("Player " + str(self.playerList[whoseTempTurn].name) + " has to move backwards! Roll the dice", (0, 0, 0))
        else:
            self.players_turn("Player "+str(self.playerList[whoseTurn].name)+" turn", (0, 0, 0))


    def addBoard(self):
        self.board = playBoard(self.screen)

    def addButton(self, text, posx, posy, width = 600, height = 100):
        self.buttonList.append(MenuButton(self.screen, text, posx, posy, width, height))

    def addLabel(self, text, posx, posy, size = 50, color = (200, 200, 200)):
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))

    def addPlayer(self, color, name, posx, posy, skinpath, state):
        self.playerList.append(Player(self.screen, color, name, posx, posy, skinpath, state))

    def addDice(self, name, posx, posy, width = 100, height = 100):
        self.dice = MenuButton(self.screen, name, posx, posy, width, height)

    def addDirection(self, text, posx, posy, width = 100, height = 100):
        self.direction = MenuButton(self.screen, text, posx, posy, width, height)

    def players_turn(self, msg, color):
        screen_text = self.font.render(msg, True, color)
        self.screen.blit(screen_text, (10, 575))
        pygame.display.update()

    def round(self, msg, color):
        screen_text = self.font.render(msg, True, color)
        self.screen.blit(screen_text, (10, 545))
        pygame.display.update()

    def explain(self, msg, msg2,msg3, color):
        screen_text = self.font.render(msg, True, color)
        self.screen.blit(screen_text, (10, 605))
        screen_text2 = self.font.render(msg2, True, color)
        self.screen.blit(screen_text2, (10, 635))
        screen_text3 = self.font.render(msg3, True, color)
        self.screen.blit(screen_text3, (10, 665))
        pygame.display.update()

class Menu:
    def __init__(self, p):
        self.p = p
        self.set_screen()
        self.background = (24, 147, 60)
        self.width, self.height = self.screen.get_size()
        self.buttonList = []
        self.labelList = []
        self.actionList = []
        self.checkboxList = []

    def addCheckbox(self, prop, posx, posy):
        width = int(self.width / 51.2)
        height = int(self.height / 28.8)
        isChecked = self.p.get(prop, "bool")
        self.checkboxList.append(MenuCheckbox(self.screen, isChecked, posx, posy, width, height))

    def set_screen(self):
        flags = 0x0
        width = self.p.get("width", "int")
        height = self.p.get("height", "int")
        if self.p.get("doublebuffering", "bool"):
            flags |= pygame.DOUBLEBUF
        if self.p.get("fullscreen", "bool"):
            flags |= pygame.FULLSCREEN
        if self.p.get("resizable", "bool"):
            flags |= pygame.RESIZABLE
        self.screen = pygame.display.set_mode((width, height), flags)
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()

    def draw(self):
        self.screen.fill(self.background)
        for button in self.buttonList:
            button.draw()
        for label in self.labelList:
            label.draw()
        for action in self.actionList:
            action.draw()
        for checkbox in self.checkboxList:
            checkbox.draw()

    def addButton(self, text, posx, posy, width = 600, height = 100):
        self.buttonList.append(MenuButton(self.screen, text, posx, posy, width, height))

    def addLabel(self, text, posx, posy, size = 50, color = (200, 200, 200)):
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))

    def addLabel1(self, text, posx, posy, size=35, color=(200, 200, 200)):
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))

    def addPlayerButton(self, text, posx, posy, width = 100, height = 100):
        self.actionList.append(MenuButton(self.screen, text, posx, posy, width, height))

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
class score:
    def __init__(self,first_name,first_score,second_name,second_score,third_name,third_score):
        self.Firstname = first_name
        self.Firstscore = first_score
        self.Secondname = second_name
        self.Secondscore = second_score
        self.Thirdname = third_name
        self.Thirdscore = third_score

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
        self.labelObject = self.renderer.render(self.text, True, self.color)
        """draw Label object if position is set"""
        if not (self.posx is None or self.posy is None):
            self.screen.blit(self.labelObject, (self.posx, self.posy))
        else:
            print("Position of a label is not set.")

class MenuCheckbox:
    def __init__(self, screen, isChecked, posx, posy, width, height):
        self.isChecked = isChecked
        self.screen = screen
        self.rect = pygame.Rect(posx, posy, width, height)

    def draw(self):
        if not self.isChecked:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 5)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)

    def __bool__(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if (mouseX > self.rect.x and mouseX < (self.rect.x+self.rect.width)) and (mouseY > self.rect.y and mouseY < (self.rect.y+self.rect.height)):
            return True
        else:
            return False

class QuestionScreen:
    def __init__(self,screen, p, playerObj):
        self.screen = screen
        self.timer = Timer(self.screen, 25, 25)
        self.player = playerObj
        self.width = p.get("width", "int")
        self.height = p.get("height", "int")
        self.gameReturn = False
        self.isComplete = False
        self.category = self.player.category
        self.rand_question_pack = db.download_per_category(self.player.category)[Random().randint(0, 14)]
        self.question = [self.rand_question_pack[2][i:i+40] for i in range(0, len(self.rand_question_pack[2]), 40)]
        self.m = Menu(p)
        self.m.addLabel("Question: ", int(self.width / 8), 25, size=30)
        i = 25
        for part in self.question:
            self.m.addLabel(part, int(self.width/4), i, size=30)
            i += 30
        self.m.addButton("A", int(self.width / 8), 200, width=275, height=75)  # Add buttons to the screen
        self.m.addLabel("Answer A: "+db.download_singlequestionoptionA(int(self.rand_question_pack[0]))[0][0], int(self.width / 2.75), 200, size=20)
        self.m.addButton("B", int(self.width / 8), 350, width=275, height=75)
        self.m.addLabel("Answer B: "+db.download_singlequestionoptionB(int(self.rand_question_pack[0]))[0][0], int(self.width / 2.75), 350, size=20)
        if self.rand_question_pack[5] is not "":
            self.m.addButton("C", int(self.width / 8), 500, width=275, height=75)
            self.m.addLabel("Answer C: "+db.download_singlequestionoptionC(int(self.rand_question_pack[0]))[0][0], int(self.width / 2.75), 500, size=20)

    def run(self):
        while not self.gameReturn:
            self.draw()
            pygame.display.flip()

            if self.timer.get_time() is 50:
                self.gameReturn = True

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type is pygame.MOUSEBUTTONUP:
                    if self.m.buttonList[0]:
                        if db.download_question_answer(self.rand_question_pack[0])[0][0] is "A":
                            self.isComplete = True
                        self.gameReturn = True
                    elif self.m.buttonList[1]:
                        if db.download_question_answer(self.rand_question_pack[0])[0][0] is "B":
                            self.isComplete = True
                        self.gameReturn = True
                    elif len(self.m.buttonList) is 3:
                        if self.m.buttonList[2]:
                            if db.download_question_answer(self.rand_question_pack[0])[0][0] is "C":
                                self.isComplete = True
                            self.gameReturn = True

        if self.isComplete:  # return statements can be replaced with "move" function in player class to move position of player instead of returning a boolean.
            return True
        else:
            return False


    def draw(self):
        self.m.draw()
        self.timer.get_label().draw()


class Timer:
    def __init__(self, screen, posx = 0, posy = 0):
        self.posx = posx
        self.posy = posy
        self.time = pygame.time.get_ticks()
        self.screen = screen
        pass

    def get_time(self):
        return int((pygame.time.get_ticks() - self.time)/1000)

    def get_label(self):
        return Label(self.screen, str(int(self.get_time())), self.posx, self.posy)

    def reset(self):
        self.time = pygame.time.get_ticks()


scores = score(db.download_top_score()[0][0], db.download_top_score()[0][1], db.download_top_score()[1][0],
               db.download_top_score()[1][1], db.download_top_score()[2][0], db.download_top_score()[2][1])

if __name__ == '__main__':
    Game().run()
