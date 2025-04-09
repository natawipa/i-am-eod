import pygame
from config import Config


class Drawer:
    # Load assets using Config
    strike_led = pygame.image.load(Config.assets['strike_led'])
    display_bg = pygame.image.load(Config.assets['display_bg'])
    main_bg = pygame.image.load(Config.assets['main_bg'])
    module_bg = pygame.image.load(Config.assets['module_bg'])
    bar = pygame.image.load(Config.assets['bar'])

    # Load elements for the password module
    stage_led = pygame.image.load(Config.assets['stage_led'])
    button = pygame.image.load(Config.assets['button'])
    clicked_button = pygame.image.load(Config.assets['clicked_button'])

    # Load wire images for each color
    wire_socket = pygame.image.load(Config.assets['wire_socket'])
    wire_images = {color: pygame.image.load(path) for color, path in Config.assets['wires'].items()}
    cutted_wire_images = {color: pygame.image.load(path) for color, path in Config.assets['cutted_wires'].items()}

    # Define button rectangles
    start_button_rect = pygame.Rect(100, 250, 400, 100)
    exit_button_rect = pygame.Rect(100, 400, 400, 100)

    # Define replay and exit button rectangles for the end screen
    replay_button_rect = pygame.Rect(100, 300, 400, 100)
    end_button_rect = pygame.Rect(100, 450, 400, 100)

    @staticmethod
    def render_menu(screen, font):
        screen.blit(Drawer.main_bg, (0, 0))

        # Draw "Start Game" button
        screen.blit(Drawer.bar, Drawer.start_button_rect.topleft)
        start_text = font.render("Start Game", True, Config.color['black'])
        start_text_rect = start_text.get_rect(center=(Drawer.start_button_rect.centerx, Drawer.start_button_rect.centery - 10))
        screen.blit(start_text, start_text_rect)

        # Draw "Exit" button
        screen.blit(Drawer.bar, Drawer.exit_button_rect.topleft)
        exit_text = font.render("Exit", True, Config.color['black'])
        exit_text_rect = exit_text.get_rect(center=(Drawer.exit_button_rect.centerx, Drawer.exit_button_rect.centery - 10))
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

    @staticmethod
    def render_end_screen(screen, font, game_result):
        """
        Render the end screen with a semi-transparent overlay, game result text, and buttons.
        """
        screen.blit(Drawer.main_bg, (0, 0))

        # Create a semi-transparent black overlay
        overlay = pygame.Surface((Config.window_width, Config.window_height))
        overlay.set_alpha(150)  # Set transparency level
        overlay.fill((0, 0, 0))  # Black color
        screen.blit(overlay, (0, 0))

        # Display game result text
        result_text = "Bomb Defused!" if game_result == "defused" else "Bomb Exploded!"
        result_color = Config.color['green'] if game_result == "defused" else Config.color['red']
        result_font = pygame.font.Font(Config.assets['font'], 60)
        result_surface = result_font.render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(Config.window_width // 2, Config.window_height // 4))
        screen.blit(result_surface, result_rect)

        # Draw "Replay" button
        screen.blit(Drawer.bar, Drawer.replay_button_rect.topleft)
        replay_text = font.render("Replay", True, Config.color['black'])
        replay_text_rect = replay_text.get_rect(center=(Drawer.replay_button_rect.centerx, Drawer.replay_button_rect.centery - 10))
        screen.blit(replay_text, replay_text_rect)

        # Draw "Exit" button
        screen.blit(Drawer.bar, Drawer.end_button_rect.topleft)
        exit_text = font.render("Exit", True, Config.color['black'])
        exit_text_rect = exit_text.get_rect(center=(Drawer.end_button_rect.centerx, Drawer.end_button_rect.centery - 10))
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

    @staticmethod
    def draw_bomb(screen, bomb):
        screen.blit(Drawer.main_bg, (0, 0))
        Drawer.draw_timer(screen, bomb)
        Drawer.draw_strike(screen, bomb)
        bomb.modules[bomb.current_module].draw(screen)

    @staticmethod
    def draw_timer(screen, bomb):
        timer_font = pygame.font.Font(Config.assets['font'], 95)
        minutes = int(bomb.time_left() // 60)
        seconds = int(bomb.time_left() % 60)
        timer_text = timer_font.render(f'{minutes:02}:{seconds:02}', True, Config.color['white'])
        screen.blit(timer_text, (60, 70))

    @staticmethod
    def draw_strike(screen, bomb):
        strike_color = Config.color['green'] if bomb.strikes == 0 else Config.color['yellow'] if bomb.strikes == 1 else Config.color['red']
        led_rect = Drawer.strike_led.get_rect(center=(520, 100))
        pygame.draw.circle(screen, strike_color, led_rect.center, led_rect.width // 2 - 2)
        screen.blit(Drawer.strike_led, led_rect)

    @staticmethod
    def draw_password_module(screen, module):
        screen.blit(Drawer.module_bg, (50, 200))
        Drawer.draw_display(screen, module)
        Drawer.draw_buttons(screen, module)
        Drawer.draw_stage_bar(screen, module)

    @staticmethod
    def draw_display(screen, module):
        display_font = pygame.font.Font(Config.assets['font'], 120)
        display_text = display_font.render(str(module.display_numbers[module.current_stage - 1]), True, Config.color['white'])
        button_margin = 20
        total_button_width = (4 * Config.button_width + 3 * button_margin)
        display_rect = pygame.Rect(110, 310, total_button_width, 170)
        screen.blit(Drawer.display_bg, (110, 310))
        display_text_rect = display_text.get_rect(center=display_rect.center)
        screen.blit(display_text, display_text_rect)

    @staticmethod
    def draw_buttons(screen, module):
        button_y = 510
        width_x = 600
        button_margin = 20
        module.buttons.clear()
        for i, label in enumerate(module.button_positions[module.current_stage - 1]):
            button_x = width_x // 2 - (2 * Config.button_width + 1.5 * button_margin) + i * (Config.button_width + button_margin)
            button_rect = pygame.Rect(button_x, button_y, Config.button_width, Config.button_height)
            screen.blit(Drawer.button, button_rect)
            button_text = module.font.render(str(label), True, Config.color['black'])
            button_text_rect = button_text.get_rect(center=(button_rect.centerx, button_rect.centery - 10))
            screen.blit(button_text, button_text_rect)
            module.buttons.append((button_rect, label))   

    @staticmethod
    def draw_stage_bar(screen, module):
        stage_x = 300
        stage_y = 265
        for i in range(module.stages):
            bar_color = Config.color['green'] if i < module.current_stage else Config.color['white']
            pygame.draw.rect(screen, bar_color, (stage_x + i * (Config.stage_led_size + 10), stage_y, Config.stage_led_size, Config.stage_led_size), 0, 9)
            screen.blit(Drawer.stage_led, (stage_x + i * (Config.stage_led_size + 10), stage_y))
            
    @staticmethod
    def update_button(screen, button_rect, label, font):
        """
        Animates a button press by briefly displaying the clicked image.
        """
        # Clear the button area
        pygame.draw.rect(screen, (205, 205, 194), button_rect)

        # Draw the clicked button image
        screen.blit(Drawer.clicked_button, button_rect)
        button_text = font.render(str(label), True, Config.color['black'])
        button_text_rect = button_text.get_rect(center=(button_rect.centerx, button_rect.centery - 5))
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()

        # Wait for a short duration to simulate animation
        pygame.time.delay(200)

        # Redraw the original button image
        screen.blit(Drawer.button, button_rect)
        button_text = font.render(str(label), True, Config.color['black'])
        button_text_rect = button_text.get_rect(center=(button_rect.centerx, button_rect.centery - 10))
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()

    @staticmethod
    def draw_wire_module(screen, module):
        screen.blit(Drawer.module_bg, (50, 200))
        module.wire_rects = []
        wire_spacing = 400 // (module.wire_num + 1)
        for i, color in enumerate(module.wires):
            # Draw the wire sockets (left)
            screen.blit(Drawer.wire_socket, (120, 240 + (i + 1) * wire_spacing))
            # Flip the image (right)
            Drawer.wire_socket = pygame.transform.flip(Drawer.wire_socket, True, False)
            screen.blit(Drawer.wire_socket, (440, 240 + (i + 1) * wire_spacing))
            # Flip the image back
            Drawer.wire_socket = pygame.transform.flip(Drawer.wire_socket, True, False)

            wire_rect = pygame.Rect(120, 235 + (i + 1) * wire_spacing, 360, 45)
            if i in module.cut_indices:  # If cut
                screen.blit(Drawer.cutted_wire_images[color], (140, 235 + (i + 1) * wire_spacing))
            else:  # If uncut
                screen.blit(Drawer.wire_images[color], (140, 235 + (i + 1) * wire_spacing))
            module.wire_rects.append(wire_rect)

            # # Debug: Draw the wire rectangle outline
            # pygame.draw.rect(screen, (255, 0, 0), wire_rect, 2)  # Red outline with 2px thickness
            
    @staticmethod
    def update_wire(screen, wire_index, module):
        """
        Marks a wire as cut and updates the screen permanently.
        """
        if wire_index not in module.cut_indices:
            module.cut_indices.append(wire_index)
        Drawer.draw_wire_module(screen, module)
        pygame.display.flip()
        