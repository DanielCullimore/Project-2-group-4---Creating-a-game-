import pygame
import sys
import pygame.gfxdraw
import configparser


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.p = Properties()
        self.set_screen()
        self.fps = 60
        self.gameExit = False
        self.clock = pygame.time.Clock()
        self.initDict()  # creates self.dict attribute containing all menu's
        self.state = self.dict['main_m']

    def run(self):
        while not self.gameExit:
            for key in self.dict:
                if self.dict[key] is self.state:
                    self.dict[key].draw()

            pygame.display.flip()

            self.clock.tick(self.fps)
            pygame.display.set_caption("Project 2 - FPS: "+str(int(self.clock.get_fps())))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type is pygame.MOUSEBUTTONUP or event.type is pygame.KEYUP:
                    self.button_functions(event)
                if event.type is pygame.VIDEORESIZE:
                    for key in self.dict:
                        if self.dict[key] is self.state:
                            temp = key
                    self.dict.clear()
                    if event.h < 480 or event.w < 640:
                        self.p.set("width", "1024")
                        self.p.set("height", "768")
                    else:
                        self.p.set("width", str(event.w))
                        self.p.set("height", str(event.h))
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict[temp]

        pygame.quit()
        sys.exit()

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

    def initDict(self):
        self.dict = {'main_m': Menu(self.p),
                     'play_m': Menu(self.p),
                     'sp_m': Menu(self.p),
                     'options_m': Menu(self.p)}
        self.dict['main_m'].addButton("Play", int(self.width/3.75), int(self.height/10*1))
        self.dict['main_m'].addButton("Options", int(self.width/3.75), int(self.height/10*3))
        self.dict['main_m'].addButton("Rules", int(self.width/3.75), int(self.height/10*5))
        self.dict['main_m'].addButton("Exit", int(self.width/3.75), self.height/10*7)
        self.dict['play_m'].addButton("Single Player", int(self.width/3.75), int(self.height/10*1))
        self.dict['play_m'].addButton("Back", int(self.width/3.75), int(self.height/10*3))
        self.dict['sp_m'].addLabel("Opponents: ", int(self.width/40*1), int(self.height/40*5))
        self.dict['sp_m'].addButton(" 2 ", int(self.width/40*15), int(self.height/10*1), int(self.width/12.8), int(self.height/7.2))
        self.dict['sp_m'].addButton(" 3 ", int(self.width/40*19), int(self.height/10*1), int(self.width/12.8), int(self.height/7.2))
        self.dict['sp_m'].addButton(" 4 ", int(self.width/40*23), int(self.height/10*1), int(self.width/12.8), int(self.height/7.2))
        self.dict['sp_m'].addButton("Back", int(self.width/3.75), int(self.height/10*3))
        self.dict['options_m'].addLabel("Fullscreen: ", int(self.width/10*4), int(self.height/10*1), size=int(self.height/36))
        self.dict['options_m'].addCheckbox("fullscreen", int(self.width/10*6), int(self.height/10*1))
        self.dict['options_m'].addLabel("DoubleBuffering: ", int(self.width/10*4), int(self.height/10*2), size=int(self.height/36))
        self.dict['options_m'].addCheckbox("doublebuffering", int(self.width/10*6), int(self.height/10*2))
        self.dict['options_m'].addLabel("Resizable: ", int(self.width/10*4), int(self.height/10*3), size=int(self.height/36))
        self.dict['options_m'].addCheckbox("resizable", int(self.width/10*6), int(self.height/10*3))
        self.dict['options_m'].addButton("Back", int(self.width/3.75), int(self.height/10*7))


    def button_functions(self, event):
        if self.state is self.dict['main_m']:
            if self.state.buttonList[3]:
                self.gameExit = True
            elif self.state.buttonList[0]:
                self.state = self.dict['play_m']
            elif self.state.buttonList[1]:
                self.state = self.dict['options_m']
        elif self.state is self.dict['play_m']:
            if self.state.buttonList[1]:
                self.state = self.dict['main_m']
            elif self.state.buttonList[0]:
                self.state = self.dict['sp_m']
        elif self.state is self.dict['sp_m']:
            if self.state.buttonList[0]:
                SinglePlayer(self.p, self.fps, 2).run()
                self.dict.clear()
                self.set_screen()
                self.initDict()
                self.state = self.dict["main_m"]
            elif self.state.buttonList[1]:
                SinglePlayer(self.p, self.fps, 3).run()
                self.dict.clear()
                self.set_screen()
                self.initDict()
                self.state = self.dict["main_m"]
            elif self.state.buttonList[2]:
                SinglePlayer(self.p, self.fps, 4).run()
                self.dict.clear()
                self.set_screen()
                self.initDict()
                self.state = self.dict["main_m"]
            elif self.state.buttonList[3]:
                self.state = self.dict['play_m']
        elif self.state is self.dict['options_m']:
            if self.state.buttonList[0]:
                self.state = self.dict['main_m']
            elif self.state.checkboxList[0] and not self.state.checkboxList[2].isChecked:
                if self.state.checkboxList[0].isChecked:
                    self.dict.clear()
                    self.p.set("fullscreen", "False")
                    self.p.set("width", "1280")
                    self.p.set("height", "720")
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict['options_m']
                    self.state.checkboxList[0].isChecked = False
                else:
                    self.dict.clear()
                    self.p.set("fullscreen", "True")
                    self.p.set("width", "1920")
                    self.p.set("height", "1080")
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict['options_m']
                    self.state.checkboxList[0].isChecked = True
            elif self.state.checkboxList[1]:
                if self.state.checkboxList[1].isChecked:
                    self.dict.clear()
                    self.p.set("doublebuffering", "False")
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict['options_m']
                    self.state.checkboxList[1].isChecked = False
                else:
                    self.dict.clear()
                    self.p.set("doublebuffering", "True")
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict['options_m']
                    self.state.checkboxList[1].isChecked = True
            elif self.state.checkboxList[2] and not self.state.checkboxList[0].isChecked:
                if self.state.checkboxList[2].isChecked:
                    self.dict.clear()
                    self.p.set("resizable", "False")
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict['options_m']
                    self.state.checkboxList[2].isChecked = False
                else:
                    self.dict.clear()
                    self.p.set("resizable", "True")
                    self.set_screen()
                    self.initDict()
                    self.state = self.dict['options_m']
                    self.state.checkboxList[2].isChecked = True


class Menu:
    def __init__(self, p):
        self.p = p
        self.set_screen()
        self.width, self.height = self.screen.get_size()
        self.background = (24, 147, 60)
        self.buttonList = []
        self.labelList = []
        self.checkboxList = []

    def draw(self):
        self.screen.fill(self.background)
        for button in self.buttonList:
            button.draw()
        for label in self.labelList:
            label.draw()
        for checkbox in self.checkboxList:
            checkbox.draw()

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

    def addButton(self, text, x, y, width = None, height = None):
        if width is None or height is None:
            width = self.width/2.13
            height = self.height/7.2
        self.buttonList.append(MenuButton(self.screen, text, x, y, width, height))

    def addLabel(self, text, posx, posy, size = None, color = (200, 200, 200)):
        if size is None:
            size = int(self.height/14.4)
        self.labelList.append(Label(self.screen, text, posx, posy, size, color))

    def addCheckbox(self, prop, posx, posy):
        width = int(self.width/51.2)
        height = int(self.height/28.8)
        isChecked = self.p.get(prop, "bool")
        self.checkboxList.append(MenuCheckbox(self.screen, isChecked, posx, posy, width, height))


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


class SinglePlayer:

    def __init__(self, p, fps, playerAmount):
        self.width = pygame.display.get_surface().get_size()[0]
        self.height = pygame.display.get_surface().get_size()[1]
        self.p = p
        self.playerAmount = playerAmount
        self.set_screen()
        self.gameReturn = False
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("res/spelbord.jpg")
        self.backgroundtransformed = pygame.transform.scale(self.background, (int(self.width * 0.5), int(self.height) - 200))
        self.fps = fps
        self.players = [Player(self.screen, "res/red_player.png", (300, 600)),Player(self.screen, "res/yellow_player.png", (600, 600))]
        self.players[0].isLocked = True
        self.state = "self"
        self.initScreens()

    def run(self):
        while not self.gameReturn:
            if self.state is "self":
                self.draw()
            elif self.state is "pause_m":
                self.dict['pause_m'].draw()
            elif self.state is "options_m":
                self.dict['options_m'].draw()

            pygame.display.flip()
            self.clock.tick(self.fps)
            pygame.display.set_caption("Project 2 - FPS: " + str(int(self.clock.get_fps())))
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type is pygame.KEYUP:
                    if event.key is pygame.K_ESCAPE:
                        if self.state is "self":
                            self.state = "pause_m"
                        elif self.state is "pause_m":
                            self.state = "self"
                if event.type is pygame.MOUSEBUTTONUP and (self.state is "pause_m" or "options_m"):
                    self.button_functions()

                if event.type is pygame.VIDEORESIZE:
                    self.dict.clear()
                    if event.h < 480 or event.w < 640:
                        self.p.set("width", "1024")
                        self.p.set("height", "768")
                    else:
                        self.p.set("width", str(event.w))
                        self.p.set("height", str(event.h))
                    self.set_screen()
                    self.initScreens()

    def button_functions(self):
        if self.state is "options_m":
            if self.dict["options_m"].buttonList[0]:
                self.state = "pause_m"
            elif self.dict["options_m"].checkboxList[0] and not self.dict["options_m"].checkboxList[2].isChecked:
                if self.dict["options_m"].checkboxList[0].isChecked:
                    self.dict.clear()
                    self.p.set("fullscreen", "False")
                    self.p.set("width", "1280")
                    self.p.set("height", "720")
                    self.set_screen()
                    self.initScreens()
                    self.dict["options_m"].checkboxList[0].isChecked = False
                else:
                    self.dict.clear()
                    self.p.set("fullscreen", "True")
                    self.p.set("width", "1920")
                    self.p.set("height", "1080")
                    self.set_screen()
                    self.initScreens()
                    self.dict["options_m"].checkboxList[0].isChecked = True
            elif self.dict["options_m"].checkboxList[1]:
                if self.dict["options_m"].checkboxList[1].isChecked:
                    self.dict.clear()
                    self.p.set("doublebuffering", "False")
                    self.set_screen()
                    self.initScreens()
                    self.dict["options_m"].checkboxList[1].isChecked = False
                else:
                    self.dict.clear()
                    self.p.set("doublebuffering", "True")
                    self.set_screen()
                    self.initScreens()
                    self.dict["options_m"].checkboxList[1].isChecked = True
            elif self.dict["options_m"].checkboxList[2] and not self.dict["options_m"].checkboxList[0].isChecked:
                if self.dict["options_m"].checkboxList[2].isChecked:
                    self.dict.clear()
                    self.p.set("resizable", "False")
                    self.set_screen()
                    self.initScreens()
                    self.dict["options_m"].checkboxList[2].isChecked = False
                else:
                    self.dict.clear()
                    self.p.set("resizable", "True")
                    self.set_screen()
                    self.initScreens()
                    self.dict["options_m"].checkboxList[2].isChecked = True
        elif self.state is "pause_m":
            if self.dict["pause_m"].buttonList[0]:
                self.state = "self"
            elif self.dict["pause_m"].buttonList[1]:
                self.state = "options_m"
            elif self.dict["pause_m"].buttonList[2]:
                self.gameReturn = True

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

    def initScreens(self):
        self.backgroundtransformed = pygame.transform.scale(self.background, (int(self.width * 0.5), int(self.height) - 200))
        self.dict = {"pause_m": Menu(self.p), "options_m": Menu(self.p)}
        width, height = self.screen.get_size()
        self.dict['pause_m'].addButton("Resume", int(width/3.75), int(height/10*1))
        self.dict['pause_m'].addButton("Options", int(width/3.75), int(height/10*3))
        self.dict['pause_m'].addButton("Exit", int(width/3.75), int(height/10*5))
        self.dict['options_m'].addLabel("Fullscreen: ", int(self.width/10*4), int(self.height/10*1), size=int(self.height/36))
        self.dict['options_m'].addCheckbox("fullscreen", int(self.width/10*6), int(self.height/10*1))
        self.dict['options_m'].addLabel("DoubleBuffering: ", int(self.width/10*4), int(self.height/10*2), size=int(self.height/36))
        self.dict['options_m'].addCheckbox("doublebuffering", int(self.width/10*6), int(self.height/10*2))
        self.dict['options_m'].addLabel("Resizable: ", int(self.width/10*4), int(self.height/10*3), size=int(self.height/36))
        self.dict['options_m'].addCheckbox("resizable", int(self.width/10*6), int(self.height/10*3))
        self.dict['options_m'].addButton("Back", int(self.width/3.75), int(self.height/10*7))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.backgroundtransformed, (self.width/4, 100))
        pygame.draw.rect(self.screen,(200,200,200),pygame.Rect(0, self.height-self.height/9, self.width, self.height))
        pygame.draw.rect(self.screen, (150, 150, 150), pygame.Rect(0, self.height-self.height/32, self.width, self.height))
        pygame.draw.rect(self.screen, (255, 255, 0), (int(self.width / 64 * 17), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (255, 255, 0), (int(self.width / 64 * 21), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (0, 0, 255), (int(self.width / 64 * 25), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (0, 0, 255), (int(self.width / 64 * 29), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (255, 0, 0), (int(self.width / 64 * 33), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (255, 0, 0), (int(self.width / 64 * 37), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (0, 255, 0), (int(self.width / 64 * 41), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        pygame.draw.rect(self.screen, (0, 255, 0), (int(self.width / 64 * 45), int(self.height-self.height/9), int(self.width/30), int(self.height/13)))
        self.players.sort(key=lambda x: x.playerPosY)
        for player in self.players:
            player.update()


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, skinPath, startPosition):
        pygame.sprite.Sprite.__init__(self)
        self.playerPosX = startPosition[0]
        self.playerPosY = startPosition[1]
        self.screen = screen
        self.ss = Spritesheet(skinPath, 5, 4, (200, 200))
        self.isLocked = False  # lock the movement of the player (useful when starting the game.)
        self.playerSpeed = 4
        self.image = self.ss.get_sprite(0, 0)  # Holds the actual surface object
        self.frame = 1  # holds the frame index which is to be drawn.
        self.threshold = 0  # holds the number of times the image will be drawn before switching frame.
        self.lastState = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.rect = self.screen.blit(self.image, (self.playerPosX, self.playerPosY))
        self.threshold += 1
        if self.threshold is 8:
            self.threshold = 0
            if self.frame is self.ss.maxColumns-1:
                self.frame = 1
            else:
                self.frame += 1
        if not self.isLocked:
            if pygame.key.get_pressed()[pygame.K_UP] and self.playerPosY>=(self.screen.get_size()[1]-125):
                self.image = self.ss.get_sprite(self.frame, 2)
                self.playerPosY -= self.playerSpeed
                self.lastState = 2
            elif pygame.key.get_pressed()[pygame.K_DOWN] and self.playerPosY<=(self.screen.get_size()[1]-75):
                self.image = self.ss.get_sprite(self.frame, 0)
                self.playerPosY += self.playerSpeed
                self.lastState = 0
            elif pygame.key.get_pressed()[pygame.K_LEFT] and self.playerPosX>=0:
                self.image = self.ss.get_sprite(self.frame, 3)
                self.playerPosX -= self.playerSpeed
                self.lastState = 3
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and self.playerPosY<=(self.screen.get_size()[0]):
                self.image = self.ss.get_sprite(self.frame, 1)
                self.playerPosX += self.playerSpeed
                self.lastState = 1
            else:
                self.image = self.ss.get_sprite(0, self.lastState)


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


if __name__ == '__main__':
    Game().run()
