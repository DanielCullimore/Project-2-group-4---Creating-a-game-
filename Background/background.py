import pygame,time

def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


def program():
    #variabelen
    width = 1250
    height =700
    size = (width,height)

    #start pygame
    pygame.init()

    #background
    background = pygame.image.load("background.jpg")

    #scale background
    backgroundtransformed = pygame.transform.scale(background,(int(width * 0.5),int(height)))

    #resolution
    screen = pygame.display.set_mode(size)

    while not process_events():
        screen.fill((255,255,255))
        screen.blit(backgroundtransformed,(0,0))

        pygame.display.flip()

program()

