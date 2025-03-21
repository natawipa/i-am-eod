import pygame
from bomb import Bomb
from drawer import Drawer
from config import Config

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.window_width, Config.window_height))
        pygame.display.set_caption(Config.window_title)
        self.clock = pygame.time.Clock()
        self.bomb = Bomb()
        self.running = True
        self.in_menu = True
        self.font = pygame.font.Font(Config.assets['font'], 50)


    def run(self):
        while self.running:
            if self.in_menu:
                self.handle_menu_events()
                Drawer.render_menu(self.screen, self.font)
            else:
                if self.bomb.game_id is None:
                    self.bomb.initialize_game_id()
                self.bomb.start_timer()
                while self.running and not self.in_menu:
                    self.handle_events()
                    self.update()
                    self.render()
                    self.clock.tick(30)

        pygame.quit()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check collision with the start button
                if Drawer.start_button_rect.collidepoint(mouse_pos):
                    self.in_menu = False  # Start the game
                # Check collision with the exit button
                elif Drawer.exit_button_rect.collidepoint(mouse_pos):
                    self.running = False  # Exit the game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bomb.handle_click(event.pos, self.screen)

    def update(self):
        if self.bomb.time_left() <= 0:
            print("Time's up! Bomb exploded.")
            self.running = False
        elif self.bomb.defused:
            print("Bomb defused!")
            self.running = False

    def render(self):
        self.screen.fill(Config.color['white'])
        Drawer.draw_bomb(self.screen, self.bomb)
        pygame.display.flip()