import csv
import sys
import time
import pygame
from config import Config
from module import PasswordModule, WireModule

class Bomb:
    def __init__(self):
        self.game_id = None
        self.modules = [PasswordModule(self), WireModule(self)]
        self.current_module = 0
        self.strikes = 0
        self.defused = False
        self.timer = Config.timer_duration
        self.start_time = None

    def initialize_game_id(self):
        """Initialize the game ID when the game starts."""
        self.game_id = self.get_next_game_id()

    def get_next_game_id(self):
        game_id_file = Config.game_id_file
        try:
            with open(game_id_file, 'r') as file:
                last_id = int(file.read().strip())
        except (FileNotFoundError, ValueError):
            last_id = 0

        next_id = last_id + 1
        with open(game_id_file, 'w') as file:
            file.write(str(next_id))  # Save the new game_id
        return next_id

    def start_timer(self):
        self.start_time = time.time()
        self.modules[self.current_module].start_timer()

    def time_left(self):
        if self.start_time is None:
            return self.timer
        elapsed_time = time.time() - self.start_time
        return max(0, self.timer - elapsed_time)

    def add_strike(self):
        self.strikes += 1
        if self.strikes >= Config.max_strikes:
            self.modules[self.current_module].log_data(self.game_id)
            if self.current_module < len(self.modules) - 1:
                self.modules[self.current_module + 1].log_data(self.game_id)
            self.log_game_data(False)
            print("Game Over! Too many strikes.")
            pygame.quit()
            sys.exit()

    def module_solved(self):
        if self.current_module < len(self.modules) - 1:
            self.modules[self.current_module].end_time = time.time()
            self.modules[self.current_module].log_data(self.game_id)
            self.current_module += 1
            self.modules[self.current_module].start_timer()
        else:
            self.defused = True
            self.modules[self.current_module].end_time = time.time()
            self.modules[self.current_module].log_data(self.game_id)
            self.log_game_data(True)

    def handle_click(self, mouse_pos, screen):
        current_module = self.modules[self.current_module]
        current_module.handle_click(mouse_pos, screen)

    def log_game_data(self, is_solved):
        # Only log to game.csv when the game ends
        time_taken = int(self.timer - self.time_left())
        mistake_rate = self.strikes / len(self.modules)
        modules_completed = self.current_module + 1
        if self.strikes >= 3:
            modules_completed -= 1

        with open(Config.log_files['game'], mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.game_id, self.strikes, is_solved, time_taken, mistake_rate, modules_completed])