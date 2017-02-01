import pygame, sys
# Help screen
def help_screen():
    # Set background image
    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode([screen_width, screen_height])

    # Game rules
    game_rules = [
    "The game is played with 2 - 4 players", "There is a dice you can roll when you",
    "answer a question correctly", "If the dice returns 1 or 2 you can go 1 step in the chosen direction"
    , "3 and 4 is 2 steps in the chosen direction and 5 and 6 3 steps in the chosen direction"
    , "If a player ends up on another players hole, the player who"
    , "was already on that hole throws a dice."
    , "The number given after throwing the dice (numbers 1 to 6) is the number the player has to go down."
    , "There are four different categories, each with its own color and questions:"
    , "Blue = Sports, Green = Geography, Red = Entertainment and Yellow = History"
    ]

    rules_body_font = pygame.font.SysFont("moonspace", 20)

    # Generate surfaces
    text_surfaces = [rules_body_font.render(rule, 1, (255,255,255))]

    # Blit the text surfaces
    for index, surface in enumerate(text_surfaces):
        screen.background.bllit(surface, ((screen.width * 0.1), (index * surface.get_height()) + (int(screen.height * 0.2))))
    # Display background
    screen.surface.blit(screen, (0, 0))

    # Set PyGame clock
    clock = pygame.time.Clock()

    # Title screen loop
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.obj.collidepoint(mouse):
                    return

        # Update PyGame screen
        pygame.display.update()
        clock.tick(30)

