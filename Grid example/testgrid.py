import pygame,time
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

spotsrow0 = [[45,255],[115,255],[185,255],[255,255]]
spotsrow1 = [[45,185],[115,185],[185,185],[255,185]]
spotsrow2 = [[45,115],[115,115],[185,115],[255,115]]
spotsrow3 = [[45,45],[115,45],[185,45],[255,45]]

movesleft = 2
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

    return False


def movement(Player):
    #start row
    if Player.Position == spotsrow0[0]:
        return 0
    if Player.Position == spotsrow0[1]:
        return 1
    if Player.Position == spotsrow0[2]:
        return 2
    if Player.Position == spotsrow0[3]:
        return 3
    # first row
    if Player.Position == spotsrow1[0]:
        return 4
    if Player.Position == spotsrow1[1]:
        return 5
    if Player.Position == spotsrow1[2]:
        return 6
    if Player.Position == spotsrow1[3]:
        return 7
    #second row
    if Player.Position == spotsrow2[0]:
        return 8
    if Player.Position == spotsrow2[1]:
        return 9
    if Player.Position == spotsrow2[2]:
        return 10
    if Player.Position == spotsrow2[3]:
        return 11
    #third row
    if Player.Position == spotsrow3[0]:
        return 12
    if Player.Position == spotsrow3[1]:
        return 13
    if Player.Position == spotsrow3[2]:
        return 14
    if Player.Position == spotsrow3[3]:
        return 15

class Player:
    def __init__(self,position,color):
        self.Position = position
        self.color = color


    def update(self):
        keys = pygame.key.get_pressed()

        if 1 > 0:


            if keys[pygame.K_UP]:
                print()

                print("key up is pressed")
                value = movement(self)
                # start position to first row
                if value == 0:
                    self.Position = spotsrow1[0]
                    print(self.Position)
                elif value == 1:
                    self.Position = spotsrow1[1]
                elif value == 2:
                    self.Position = spotsrow1[2]
                elif value == 3:
                    self.Position = spotsrow1[3]
                # first row to second row
                elif value == 4:
                    self.Position = spotsrow2[0]
                elif value == 5:
                    self.Position = spotsrow2[1]
                elif value == 6:
                    self.Position = spotsrow2[2]
                elif value == 7:
                    self.Position = spotsrow2[3]
                #second row to third
                elif value == 8:
                    self.Position = spotsrow3[0]
                elif value == 9:
                    self.Position = spotsrow3[1]
                elif value == 10:
                    self.Position = spotsrow3[2]
                elif value == 11:
                    self.Position = spotsrow3[3]



            elif keys[pygame.K_RIGHT]:
                print()
                print("key right is pressed")
                value = movement(self)
                #start row
                if value == 0:
                    self.Position = spotsrow0[1]

                elif value == 1:
                    self.Position = spotsrow0[2]
                elif value == 2:
                    self.Position = spotsrow0[3]
                elif value == 3:
                    print("cannot move right")
                #first row
                elif value == 4:
                    self.Position = spotsrow1[1]
                elif value == 5:
                    self.Position = spotsrow1[2]
                elif value == 6:
                    self.Position = spotsrow1[3]
                elif value == 7:
                    print("cannot move right")
                #second row
                elif value == 8:
                    self.Position = spotsrow2[1]
                elif value == 9:
                    self.Position = spotsrow2[2]
                elif value == 10:
                    self.Position = spotsrow2[3]
                elif value == 11:
                    print("cannot move right")
                #third row
                elif value == 12:
                    self.Position = spotsrow3[1]
                elif value == 13:
                    self.Position = spotsrow3[2]
                elif value == 14:
                    self.Position = spotsrow3[3]
                elif value == 15:
                    print("Cannot move ")

            elif keys[pygame.K_LEFT]:
                print()
                print("key right is pressed")
                value = movement(self)
            #start row

                if value == 0:
                    print("Cannot move left")

                elif value == 1:
                    self.Position = spotsrow0[0]
                elif value == 2:
                    self.Position = spotsrow0[1]
                elif value == 3:
                    self.Position = spotsrow0[2]
                #first row
                elif value == 4:
                    print("Cannot move left")
                elif value == 5:
                    self.Position = spotsrow1[0]
                elif value == 6:
                    self.Position = spotsrow1[1]
                elif value == 7:
                    self.Position = spotsrow1[2]
                #second row
                elif value == 8:
                    print("Cannot move left")
                elif value == 9:
                    self.Position = spotsrow2[0]
                elif value == 10:
                    self.Position = spotsrow2[1]
                elif value == 11:
                    self.Position = spotsrow2[2]

                #third row
                elif value == 12:
                    print("Cannot move left")
                elif value == 13:
                    self.Position = spotsrow3[0]
                elif value == 14:
                    self.Position = spotsrow3[1]
                elif value == 15:
                    self.Position = spotsrow3[2]
            False






    def draw(self,screen):
        pygame.draw.circle(screen,self.color,self.Position , 5)




def program():
    # variabelen
    turn = 0
    width = 300
    height =300
    size = (width,height)




    # startpoints
    player1 = Player(spotsrow0[0], red)
    player2 = Player(spotsrow0[1], green)
    player3 = Player(spotsrow0[2], blue)
    player4 = Player(spotsrow0[3], black)


    # start pygame
    pygame.init()

    clock = pygame.time.Clock()
    # background
    background = pygame.image.load("grid.jpg")
    backgroundtransformed = pygame.transform.scale(background,(int(width),int(height)))

    # resolution
    screen = pygame.display.set_mode(size)
    #keys
    keys = pygame.key.get_pressed()
    while not process_events():
        clock.tick(15)
        screen.fill((255,255,255))

        # background/euromast
        screen.blit(backgroundtransformed,(0,0))

        # get position of mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()


        #update players

        if turn == 4:
            turn = 0

        if turn == 0:

            player1.update()




        if turn == 1:
            player2.update()



        if turn == 2:
            player3.update()



        if turn == 3:
            player4.update()



        #draw players
        player1.draw(screen)
        player2.draw(screen)
        player3.draw(screen)
        player4.draw(screen)


        # display all the changes
        pygame.display.flip()

program()

