class Config:
    # Window settings
    window_width = 600
    window_height = 750
    window_title = "I AM EOD"

    # Font and assets
    assets = {
        'font': './element/game_font.ttf',
        'strike_led': './element/strike_led.png',
        'display_bg': './element/display_bg.png',
        'main_bg': './element/main_bg.png',
        'module_bg': './element/module_bg.png',
        'bar': './element/menu_bar.png',
        'stage_led': './element/stage_led.png',
        'button': './element/button.png',
        'clicked_button': './element/button_click.png',
        'wire_socket': './element/wire_sock.png',
        'wires': {
            'red': './element/red.png',
            'blue': './element/blue.png',
            'yellow': './element/yellow.png',
            'black': './element/black.png',
            'white': './element/white.png',
        },
        'cutted_wires': {
            'red': './element/red_cut.png',
            'blue': './element/blue_cut.png',
            'yellow': './element/yellow_cut.png',
            'black': './element/black_cut.png',
            'white': './element/white_cut.png',
        }
    }

    # Colors
    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'gray': (191, 191, 191),
        'dark_gray': (50, 50, 50),
        'green': (0, 255, 0),
        'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'blue': (0, 0, 255),
        'gold': (205, 205, 194),
    }

    # Gameplay settings
    max_strikes = 3
    timer_duration = 180  # 3 minutes

    # Module settings
    module_size = 500
    strike_radius = 25
    button_width = 80
    button_height = 120
    stage_led_size = 30

    # Logging settings
    log_files = {
        'game': './logs/game.csv',
        'password': './logs/password.csv',
        'wire': './logs/wire.csv',
    }
    game_id_file = './logs/game_id.txt'

    # Background music
    bgm = './sound/Keep Talking and Nobody Explodes OST - DRAGON.wav'

    # Sound effects
    sfx = {
        'button_click': './sound/click.wav',
        'strike': './sound/strike.wav',
        'defuse': './sound/defuse.wav',
        'explosion': './sound/explosion.wav',
    }
    