import pygame
pygame.mixer.init()

"""
10 Kanäle für Sounds initialisieren
"""
pygame.mixer.set_num_channels(10) #Anzahl der gleichzeitig abspielbaren Sounds

"""
weisst jedem Sound eine Variabel und Datei zu,damit sie im Spiel verwendet werden können und übereinenader 
abgespielt werden können.
"""
slow_theme = pygame.mixer.Sound(r"Main\sounds\slow_themes.mp3")
pilz_abbauen = pygame.mixer.Sound(r"Main\sounds\water-bubbles-257594.wav")
fackelsound = pygame.mixer.Sound(r"Main\sounds\breath-264957-1.wav")
bubble_pop = pygame.mixer.Sound(r"Main\sounds\bubble-pop-293342-_1_.wav")
sword_slice= pygame.mixer.Sound(r"Main\sounds\sword-slice-393847-_1_.wav")
monkey_noise = pygame.mixer.Sound(r"Main\sounds\monkey-noise-sound-effect-no-copyright-390901-_1_.wav")
walking_main_character = pygame.mixer.Sound(r"Main\sounds\foot-steps-77348-1.wav")
crafting_axe = pygame.mixer.Sound(r"Main\sounds\crafting_sound_axe.wav")
laser_aus_sound = pygame.mixer.Sound(r"Main\sounds\laser_aus.wav")
crafting_torche = pygame.mixer.Sound(r"Main\sounds\fackel_craften.wav")

"""
weist den Sounds verschiedene Channels zu, damit sie gleichzeitig abgespielt werden können
"""
channel_background = pygame.mixer.Channel(0)
channel_water = pygame.mixer.Channel(1)
channel_breath = pygame.mixer.Channel(2)
channel_bubble_pop = pygame.mixer.Channel(3)
channel_sword = pygame.mixer.Channel(4)
channel_monkey = pygame.mixer.Channel(5)
channel_walk = pygame.mixer.Channel(6)
channel_crafting = pygame.mixer.Channel(7)
channel_fackelsound = pygame.mixer.Channel(8)
channel_laser_aus = pygame.mixer.Channel(9)

"""
Hintergrundmusik (IMPLEMENTIERT)
"""
def play_background_music(): 
    channel_background.set_volume(0.05)
    channel_background.play(slow_theme, loops=-1)  

"""
beim abauen der Pilzes (x)
"""
def play_pilz_abbauen():
    channel_water.set_volume(0.1)
    channel_water.play(pilz_abbauen)

"""
Sound, sobald man eine Fackel in der Hand hält (x)
"""
def play_fackelsound(): 
    channel_fackelsound.set_volume(0.1)
    channel_fackelsound.play(fackelsound)

"""
Sound für das aufsammeln von Items (IMPLEMENTIERT)
"""
def play_bubble_pop(): 
    channel_bubble_pop.set_volume(0.9)
    channel_bubble_pop.play(bubble_pop)
    print("bubble_pop")

"""
Sound für das schwingen des Schwertes (IMPLEMENTIERT)
"""
def play_sword_slice(): 
    channel_sword.set_volume(0.1)
    channel_sword.play(sword_slice)

"""
Sound für die Endanimation (x)
"""
def play_monkey_noise(): 
    channel_monkey.set_volume(0.1)
    channel_monkey.play(monkey_noise)

"""
Sound für das Laufen des Hauptcharakters (IMPLEMENTIERT)
"""
def play_walking_main_character(): 
    channel_walk.set_volume(0.9)
    channel_walk.play(walking_main_character, loops = -1)
    print("walking_main_character")

def stop_walking_main_character():
    channel_walk.stop()

"""
Sound für das craften der Axt (x)
"""
def play_crafting_axe(): 
    channel_crafting.set_volume(0.9)
    channel_crafting.play(crafting_axe)
    print("crafting_axe")

"""
Sound für das craften der Fackel (x)
"""
def play_crafting_torche(): 
    channel_crafting.set_volume(0.9)
    channel_crafting.play(crafting_torche, maxtime=2000)
    print("crafting_torche")

"""
Sound, soblad der Laser ausgeschaltet wird (IMPLEMENTIERT)
"""
def laser_aus(): 
    channel_laser_aus.set_volume(0.6)
    channel_laser_aus.play(laser_aus_sound)
    print("laser_aus")