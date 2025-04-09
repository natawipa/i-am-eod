import pygame
from config import Config


class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.bgm_volume = 0.5
        self.sfx_volume = 0.7

    def play_bgm(self, loop=True):
        """Play background music."""
        pygame.mixer.music.load(Config.bgm)
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_bgm(self):
        """Stop background music."""
        pygame.mixer.music.stop()

    def play_sfx(self, sound_path):
        """Play a sound effect."""
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(self.sfx_volume)
        sound.play()
        