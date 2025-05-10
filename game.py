import pygame
import multiprocessing
from bomb import Bomb
from sound import Sound
from drawer import Drawer
from config import Config
from stats import Stats


def show_statistics_process():
    """Function to display game statistics in a tkinter window (runs in a separate process)."""
    viewer = Stats()
    viewer


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
        self.sound = Sound()
        self.sound.play_bgm()
        self.game_over = False
        self.game_result = None

    def run(self):
        while self.running:
            if self.in_menu:
                self.handle_menu_events()
                Drawer.render_menu(self.screen, self.font)
            elif self.game_over:
                self.handle_end_screen_events()
                Drawer.render_end_screen(self.screen, self.font, self.game_result)
            else:
                if self.bomb.game_id is None:
                    self.bomb.initialize_game_id()
                self.bomb.start_timer()
                while self.running and not self.in_menu and not self.game_over:
                    self.handle_events()
                    self.update()
                    self.render()
                    self.clock.tick(30)

        self.sound.stop_bgm()
        pygame.quit()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check collision with the start button
                if Drawer.start_button_rect.collidepoint(mouse_pos):
                    self.sound.play_sfx(Config.sfx['button_click'])
                    pygame.time.wait(200)
                    self.in_menu = False  # Start the game
                # Check collision with the exit button
                elif Drawer.exit_button_rect.collidepoint(mouse_pos):
                    self.sound.play_sfx(Config.sfx['button_click'])
                    pygame.time.wait(200)
                    self.running = False  # Exit the game
                # Check collision with the stats button
                elif Drawer.static_button_rect.collidepoint(mouse_pos):  # Assuming a stats button exists
                    self.sound.play_sfx(Config.sfx['button_click'])
                    pygame.time.wait(200)
                    # Launch the statistics viewer in a separate process
                    stats_process = multiprocessing.Process(target=show_statistics_process)
                    stats_process.start()
                # # Check collision with the tutorial button
                # elif Drawer.tutorial_button_rect.collidepoint(mouse_pos):
                #     self.sound.play_sfx(Config.sfx['button_click'])
                #     pygame.time.wait(200)
                #     # Show tutorial (not implemented in this snippet)
                #     print("Show tutorial")  # Placeholder for tutorial functionality
                    
    def handle_end_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Drawer.replay_button_rect.collidepoint(mouse_pos):
                    self.sound.play_sfx(Config.sfx['button_click'])
                    pygame.time.wait(200)
                    self.reset_game()
                elif Drawer.end_button_rect.collidepoint(mouse_pos):
                    self.sound.play_sfx(Config.sfx['button_click'])
                    pygame.time.wait(200)
                    self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bomb.handle_click(event.pos, self.screen)

    def update(self):
        if self.bomb.time_left() <= 0:
            self.game_over = True
            self.game_result = "exploded"
            print("Time's up! Bomb exploded.")
        elif self.bomb.defused:
            self.game_over = True
            self.game_result = "defused"
            print("Bomb defused!")
        elif self.bomb.strikes >= Config.max_strikes:
            self.game_over = True
            self.game_result = "exploded"
            print("Too many strikes! Bomb exploded.")

    def render(self):
        self.screen.fill(Config.color['white'])
        Drawer.draw_bomb(self.screen, self.bomb)
        pygame.display.flip()

    def reset_game(self):
        """Reset the game state for replay."""
        self.bomb = Bomb()
        self.in_menu = True
        self.game_over = False
        self.game_result = None
        