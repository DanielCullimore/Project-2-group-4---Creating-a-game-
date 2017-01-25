import pygame

Black = (0,0,255)
Green = (0,255,0)
Red = (255,0,0)
White = (255,255,255)

pygame.init()
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
font = pygame.font.SysFont('moonspace', 30)

def players_turn(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text,(10, 575))
    pygame.display.update()

players_turn("Player 1 turn", White)


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

    clock.tick(30)
    # Go ahead and update the screen with what we've drawn.

pygame.quit()