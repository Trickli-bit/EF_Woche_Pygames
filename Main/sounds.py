import pygame
pygame.mixer.init()
slow_theme = pygame.mixer.Sound(r"Main\sounds\slow_themes.mp3")

def play_background_music():
    slow_theme.set_volume(0.1)
    slow_theme.play(loops = -1)