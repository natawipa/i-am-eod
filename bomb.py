import csv
import sys
import time
import pygame
from sound import Sound
from config import Config
from module import PasswordModule, WireModule, SimonSaysModule


class Bomb:
    def __init__(self):
        self.game_id = None
        self.modules = [PasswordModule(self), WireModule(self)]
        # self.modules = [SimonSaysModule(self)]  # SimonSaysModule will be implemented later
        self.current_module = 0
        self.strikes = 0
        self.defused = False
        self.timer = Config.timer_duration
        self.start_time = None
        self.sound = Sound()
        self.game_over = False
        self.logging_in_progress = False

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
            file.write(str(next_id)) 
        return next_id

    def start_timer(self):
        self.start_time = time.time()
        self.modules[self.current_module].start_timer()

    def time_left(self):
        if self.start_time is None:
            return self.timer
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.timer and not self.game_over:
            self.modules[self.current_module].log_data(self.game_id)
            if self.current_module < len(self.modules) - 1:
                self.modules[self.current_module + 1].log_data(self.game_id)
            self.log_game_data(False, "timeout")
            self.defused = False
            self.sound.play_sfx(Config.sfx['explosion'])
            self.game_over = True 
            return 0
        return max(0, self.timer - elapsed_time)

    def add_strike(self):
        if self.game_over: 
            return
        self.sound.play_sfx(Config.sfx['strike'])
        self.strikes += 1
        if self.strikes >= Config.max_strikes:
            self.modules[self.current_module].log_data(self.game_id)
            if self.current_module < len(self.modules) - 1:
                self.modules[self.current_module + 1].log_data(self.game_id)
            self.log_game_data(False, "too many strikes")
            print("Game Over! Too many strikes.")
            self.defused = False
            self.sound.play_sfx(Config.sfx['explosion'])
            self.game_over = True

    def module_solved(self):
        if self.game_over:
            return
        if self.current_module < len(self.modules) - 1:
            self.modules[self.current_module].end_time = time.time()
            self.modules[self.current_module].log_data(self.game_id)
            self.current_module += 1
            self.modules[self.current_module].start_timer()
        else:
            self.sound.play_sfx(Config.sfx['defuse'])
            self.defused = True
            self.modules[self.current_module].end_time = time.time()
            self.modules[self.current_module].log_data(self.game_id)
            self.log_game_data(True, "defused")
            self.game_over = True  

    def handle_click(self, mouse_pos, screen):
        current_module = self.modules[self.current_module]
        current_module.handle_click(mouse_pos, screen)

    def log_game_data(self, is_solved, game_result):
        if self.logging_in_progress:
            return
        self.logging_in_progress = True

        time_taken = int(self.timer - max(0, self.timer - (time.time() - self.start_time))) 
        mistake_rate = self.strikes / len(self.modules)
        modules_completed = self.current_module + 1
        if self.strikes >= Config.max_strikes:
            modules_completed -= 1

        with open(Config.log_files['game'], mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.game_id, self.strikes, is_solved, time_taken, mistake_rate, modules_completed, game_result])

        self.logging_in_progress = False  
        