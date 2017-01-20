import pygame
import random

Black = (0,0,255)
Green = (0,255,0)
Red = (255,0,0)
Grey = (190,190,190)
White = (0,0,0)
Brown = (255,222,173)
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

players_list = pygame.sprite.Group()

player1 = Player(Brown, 20, 15)
player2 = Player(Green, 20, 15)
player3 = Player(Red, 20, 15)
player4 = Player(Grey, 20, 15)

player1.rect.x = random.randrange(screen_width)
player1.rect.y = random.randrange(screen_height)
player2.rect.x = random.randrange(screen_width)
player2.rect.y = random.randrange(screen_height)
player3.rect.x = random.randrange(screen_width)
player3.rect.y = random.randrange(screen_height)
player4.rect.x = random.randrange(screen_width)
player4.rect.y = random.randrange(screen_height)

players_list.add(player1)
players_list.add(player2)
players_list.add(player3)
players_list.add(player4)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Clear the screen
    screen.fill(White)

    # Draw all the spites
    players_list.draw(screen)

    clock.tick(30)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()