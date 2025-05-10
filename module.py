import csv
import time
import random
import pygame
from sound import Sound
from drawer import Drawer
from config import Config


class Module:
    def __init__(self, bomb):
        self.bomb = bomb
        self.is_solved = False
        self.start_time = None  # Initialize start_time for each module
        self.end_time = None
        self.sound = Sound()

    def start_timer(self):
        self.start_time = time.time()

    def handle_click(self, mouse_pos, screen):
        pass

    def draw(self, screen):
        pass

    def log_data(self, game_id):
        pass


class PasswordModule(Module):
    def __init__(self, bomb):
        super().__init__(bomb)
        self.stages = 5
        self.current_stage = 1
        self.display_numbers = [random.randint(1, 4) for _ in range(self.stages)]
        self.button_positions = [random.sample([1, 2, 3, 4], 4) for _ in range(self.stages)]
        self.solution_positions = [None] * self.stages
        self.solution_labels = [None] * self.stages
        self.buttons = []
        self.font = pygame.font.Font(Config.assets['font'], 74)
        self.get_solution()
        self.mistakes_per_stage = [0] * self.stages

    def get_solution(self):
        for stage in range(1, self.stages + 1):
            if stage == 1:
                if self.display_numbers[stage - 1] in [1, 2]:
                    self.solution_positions[stage - 1] = 2
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][1]
                elif self.display_numbers[stage - 1] == 3:
                    self.solution_positions[stage - 1] = 3
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][2]
                elif self.display_numbers[stage - 1] == 4:
                    self.solution_positions[stage - 1] = 4
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][3]
            elif stage == 2:
                if self.display_numbers[stage - 1] == 1:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(4) + 1
                    self.solution_labels[stage - 1] = 4
                elif self.display_numbers[stage - 1] in [2, 4]:
                    self.solution_positions[stage - 1] = self.solution_positions[stage - 2]
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][self.solution_positions[stage - 1] - 1]
                elif self.display_numbers[stage - 1] == 3:
                    self.solution_positions[stage - 1] = 1
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][0]
            elif stage == 3:
                if self.display_numbers[stage - 1] == 1:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(self.solution_labels[stage - 2]) + 1
                    self.solution_labels[stage - 1] = self.solution_labels[stage - 2]
                elif self.display_numbers[stage - 1] == 2:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(self.solution_labels[stage - 3]) + 1
                    self.solution_labels[stage - 1] = self.solution_labels[stage - 3]
                elif self.display_numbers[stage - 1] == 3:
                    self.solution_positions[stage - 1] = 3
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][2]
                elif self.display_numbers[stage - 1] == 4:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(4) + 1
                    self.solution_labels[stage - 1] = 4
            elif stage == 4:
                if self.display_numbers[stage - 1] == 1:
                    self.solution_positions[stage - 1] = self.solution_positions[stage - 4]
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][self.solution_positions[stage - 1] - 1]
                elif self.display_numbers[stage - 1] == 2:
                    self.solution_positions[stage - 1] = 1
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][0]
                elif self.display_numbers[stage - 1] in [3, 4]:
                    self.solution_positions[stage - 1] = self.solution_positions[stage - 3]
                    self.solution_labels[stage - 1] = self.button_positions[stage - 1][self.solution_positions[stage - 1] - 1]
            elif stage == 5:
                if self.display_numbers[stage - 1] == 1:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(self.solution_labels[stage - 5]) + 1
                    self.solution_labels[stage - 1] = self.solution_labels[stage - 5]
                elif self.display_numbers[stage - 1] == 2:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(self.solution_labels[stage - 4]) + 1
                    self.solution_labels[stage - 1] = self.solution_labels[stage - 4]
                elif self.display_numbers[stage - 1] == 3:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(self.solution_labels[stage - 2]) + 1
                    self.solution_labels[stage - 1] = self.solution_labels[stage - 2]
                elif self.display_numbers[stage - 1] == 4:
                    self.solution_positions[stage - 1] = self.button_positions[stage - 1].index(self.solution_labels[stage - 3]) + 1
                    self.solution_labels[stage - 1] = self.solution_labels[stage - 3]
            print(f"Stage {stage}: {self.display_numbers[stage - 1]} -> {self.solution_positions[stage - 1]} -> {self.solution_labels[stage - 1]}")

    def handle_click(self, mouse_pos, screen):
        for button_rect, label in self.buttons:
            if button_rect.collidepoint(mouse_pos):
                self.sound.play_sfx(Config.sfx['button_click'])
                pygame.time.wait(200)
                Drawer.update_button(screen, button_rect, label, self.font)
                if label == self.solution_labels[self.current_stage - 1]:
                    self.current_stage += 1
                    if self.current_stage > self.stages:
                        self.is_solved = True
                        self.end_time = time.time()
                        self.bomb.module_solved()
                else:
                    self.mistakes_per_stage[self.current_stage - 1] += 1
                    self.bomb.add_strike()
                    self.reset()

    def reset(self):
        self.current_stage = 1
        self.display_numbers = [random.randint(1, 4) for _ in range(self.stages)]
        self.button_positions = [random.sample([1, 2, 3, 4], 4) for _ in range(self.stages)]
        self.get_solution()

    def draw(self, screen):
        Drawer.draw_password_module(screen, self)

    def log_data(self, game_id):
        if self.end_time is None:
            self.end_time = time.time()

        time_taken = None
        if self.start_time and self.end_time:
            time_taken = int(self.end_time - self.start_time)

        with open(Config.log_files['password'], mode='a', newline='') as file:
            writer = csv.writer(file)
            # Calculate the most mistake stages
            max_mistakes = max(self.mistakes_per_stage) if self.mistakes_per_stage else 0
            most_mistake_stages = [i + 1 for i, mistakes in enumerate(self.mistakes_per_stage) if mistakes == max_mistakes] if max_mistakes > 0 else []

            # Determine stages completed
            if self.is_solved:
                stages_completed = self.stages
            else:
                # Find the last stage with a mistake
                # iterate through the mistakes_per_stage in reverse order if > 0 that index + 1 is the last stage completed
                for i in range(len(self.mistakes_per_stage) - 1, -1, -1):
                    if self.mistakes_per_stage[i] > 0:
                        stages_completed = i
                        break 

            writer.writerow([
                game_id,
                1 + sum(self.mistakes_per_stage),  # Total mistakes
                most_mistake_stages,               # Most mistake stages
                str(self.mistakes_per_stage),      # Mistakes per stage
                stages_completed,                  # Stages completed
                time_taken,                        # Time taken
                self.is_solved                     # Whether the module was solved
            ])


class WireModule(Module):
    def __init__(self, bomb):
        super().__init__(bomb)
        self.colours = ["red", "blue", "yellow", "black", "white"]
        self.wire_num = random.randint(3, 6)
        self.wires = [random.choice(self.colours) for _ in range(self.wire_num)]
        self.mistakes = 0
        self.cut_indices = []
        self.get_solution()

    def get_solution(self):
        if self.wire_num == 3:
            if self.wires.count("red") == 0:
                self.solution = 2
            elif self.wires[-1] == "white":
                self.solution = self.wire_num
            elif self.wires.count("blue") > 1:
                self.solution = max([i for i, wire in enumerate(self.wires) if wire == "blue"]) + 1
            else:
                self.solution = self.wire_num
        elif self.wire_num == 4:
            if self.wires.count("red") > 1:
                self.solution = max([i for i, wire in enumerate(self.wires) if wire == "red"]) + 1
            elif self.wires[-1] == "yellow" and self.wires.count("red") == 0:
                self.solution = 1
            elif self.wires.count("blue") == 1:
                self.solution = 1
            elif self.wires.count("yellow") > 1:
                self.solution = self.wire_num
            else:
                self.solution = 2
        elif self.wire_num == 5:
            if self.wires[-1] == "black":
                self.solution = 4
            elif self.wires.count("red") == 1 and self.wires.count("yellow") > 1:
                self.solution = 1
            elif self.wires.count("black") == 0:
                self.solution = 2
            else:
                self.solution = 1
        elif self.wire_num == 6:
            if self.wires.count("yellow") == 0:
                self.solution = 3
            elif self.wires.count("yellow") == 1 and self.wires.count("white") > 1:
                self.solution = 4
            elif self.wires.count("red") == 0:
                self.solution = self.wire_num
            else:
                self.solution = 4
        print(f"Solution: {self.solution}")

    def handle_click(self, mouse_pos, screen):
        for i, wire_rect in enumerate(self.wire_rects):
            if wire_rect.collidepoint(mouse_pos):
                if i not in self.cut_indices: 
                    self.cut_indices.append(i)
                    Drawer.update_wire(screen, i, self)
                    if i + 1 == self.solution:
                        self.is_solved = True
                        self.end_time = time.time()
                        self.bomb.module_solved()
                    else:
                        self.bomb.add_strike()
                        self.mistakes += 1
                break

    def reset(self):
        self.wire_num = random.randint(3, 6)
        self.wires = [random.choice(self.colours) for _ in range(self.wire_num)]
        self.cut_indices = []
        self.get_solution()
        
    def draw(self, screen):
        Drawer.draw_wire_module(screen, self)

    def log_data(self, game_id):
        if self.end_time is None:
            self.end_time = time.time()

        time_taken = None
        if self.start_time and self.end_time:
            time_taken = int(self.end_time - self.start_time)

        with open(Config.log_files['wire'], mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                game_id,
                len(self.cut_indices),  # Number of attempts
                self.cut_indices,       # Indices of wires cut
                [self.wires[i - 1] for i in self.cut_indices],  # Colors of wires cut
                self.wire_num,          # Number of wires in the module
                time_taken,             # Time taken to solve the module
                self.is_solved          # Whether the module was solved
            ])


class SimonSaysModule(Module):
    # Will be implemented if have time
    def __init__(self, bomb):
        pass

    def handle_click(self, mouse_pos, screen):
        pass

    def draw(self, screen):
        pass

    def log_data(self, game_id):
        pass
