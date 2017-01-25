
import pygame
import random

Black = (0,0,255)
Green = (0,255,0)
Red = (255,0,0)
Grey = (190,190,190)
White = (0,0,0)
Brown = (255,222,173)

def diceroll():
    keys = pygame.key.get_pressed()
    #change space for button on screen
    if keys[pygame.K_SPACE]:
        result = random.randrange(1,7,1)

        return result


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        #surface test(remove after it works)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

pygame.init()
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

#load image
background = pygame.image.load("Background/spelbord.jpg")
#Transform image
backgroundtransformed = pygame.transform.scale(background,(int(0.5 * screen_width),int(0.5 * screen_height)))


players_list = pygame.sprite.Group()

player1 = Player(Brown, 20, 15)
player2 = Player(Green, 20, 15)
player3 = Player(Grey, 20, 15)
player4 = Player(Red, 20, 15)

player1.rect.x = int(screen_width*0.27)
player1.rect.y = int(screen_height*0.593)
player2.rect.x = int(screen_width*0.4)
player2.rect.y = int(screen_height*0.593)
player3.rect.x = int(screen_width*0.58)
player3.rect.y = int(screen_height*0.593)
player4.rect.x = int(screen_width*0.71)
player4.rect.y = int(screen_height*0.593)

players_list.add(player1)
players_list.add(player2)
players_list.add(player3)
players_list.add(player4)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#set font
font = pygame.font.Font(None,20)


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Clear the screen
    screen.fill(White)
    #dice rolls
    diceresult = diceroll()
    dice_text = font.render("Dice result: {}".format(diceresult),1,Red)
    screen.blit(dice_text, (16, screen_height *0.95))




    #add playboard
    screen.blit(backgroundtransformed,(int(0.25 *screen_width),int(0.12*screen_height)))

    # Draw all the spites
    players_list.draw(screen)

    clock.tick(30)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
