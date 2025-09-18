import pygame
pygame.mixer.init()
slow_theme = pygame.mixer.Sound(r"Main\sounds\slow_themes.mp3")
water_bubble = pygame.mixer.Sound(r"Main\sounds\water-bubbles-257594.mp3")
breath = pygame.mixer.Sound(r"Main\sounds\breath-264957 1.mp3")
bubble_pop = pygame.mixer.Sound(r"Main\sounds\bubble-pop-293342 (1).mp3")
sword_slice= pygame.mixer.Sound(r"Main\sounds\sword-slice-393847 (1).mp3")
monkey_noise = pygame.mixer.Sound(r"Main\sounds\monkey-noise-sound-effect-no-copyright-390901 (1).mp3")
walking_main_character = pygame.mixer.Sound(r"Main\sounds\rocks-crumbling-from-room-or-cave-76827.mp3")
crafting_axe = pygame.mixer.Sound(r"Main\sounds\rock-cinematic-161648.mp3")

v = 0

def play_background_music(): #Hintergrundmusik (IMPLEMENTIERT)
    slow_theme.set_volume(v)
    slow_theme.play(loops = -1)

def play_water_bubble(): #beim abauen der Pilzes (x)
    water_bubble.set_volume(v)
    water_bubble.play()

def play_breath(): #Sound, sobald man eine Fackel in der Hand hält (x)
    breath.set_volume(v)
    breath.play()

def play_bubble_pop(): #Sound für das aufsammeln von Items (IMPLEMENTIERT)
    bubble_pop.set_volume(v)
    bubble_pop.play()

def play_sword_slice(): #beim angreifen eines Mobs (x)
    sword_slice.set_volume(v)
    sword_slice.play()

def play_monkey_noise(): #Endanimation (x)
    monkey_noise.set_volume(v)
    monkey_noise.play()

def play_walking_main_character(): #Laufsound des Hauptcharakters (IMPLEMENTIERT)
    walking_main_character.set_volume(v)
    walking_main_character.play()

def stop_walking_main_character():
    walking_main_character.stop()

def play_crafting_axe(): #Sound für das craften der Axt (IMPLEMENTIERT)
    crafting_axe.set_volume(v)
    crafting_axe.play()