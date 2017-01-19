import pygame

pygame.init()

class GameMenu():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size=30,
                 font_color=(255, 255, 255)):
        self.Screen = screen
        self.Scr_width = self.Screen.get_rect().width
        self.Scr_height = self.Screen.get_rect().height

        self.Bg_color = bg_color
        self.Clock = pygame.time.Clock()

        self.Items = items
        self.Font = pygame.font.SysFont(font, font_size)
        self.Font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.Font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.Scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.Scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def run(self):
        fps = self.Clock.tick(30)
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            # Redraw the background
            self.Screen.fill(self.Bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.Screen.blit(label, (posx, posy))

            pygame.display.flip()


if __name__ == "__main__":
    # Creating the screen
    Screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Start the game','Game settings', 'Quit the game')
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(Screen, menu_items)
    gm.run()