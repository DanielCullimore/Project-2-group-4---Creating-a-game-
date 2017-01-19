import pygame
pygame.init()

class GameMenu():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size=30,
                 font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])
    def Game_menu_loop(self):
        mainloop = True
        mpos = pygame.mouse.get_pos()
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            mainloop = False
                            self.funcs[item.text]()
                    self.screen.fill(self.bg_color)

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_mouse_selection(self, item, mpos):
        if item.is_mouse_selection(mpos):
            item.set_font_color(RED)
            item.set_italic(True)
        else:
            item.set_font_color(WHITE)
            item.set_italic(False)

        for name, label, (width, height), (posx, posy) in self.items:
            self.screen.blit(label, (posx, posy))

        pygame.display.flip()
if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480), 0, 32)
    menu_items = ('Start the game',"Settings", 'Quit the game')
    funcs = ['Start the game':sys.exit., 'Settings':sys.exit,"Quit the game":sys.exit]
    pygame.display.set_caption('Game Menu')

gm = GameMenu(screen, menu_items)
gm.Game_menu_loop()

