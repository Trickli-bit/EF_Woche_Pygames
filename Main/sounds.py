import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(10) #Anzahl der gleichzeitig abspielbaren Sounds
slow_theme = pygame.mixer.Sound(r"Main\sounds\slow_themes.mp3")
pilz_abbauen = pygame.mixer.Sound(r"Main\sounds\water-bubbles-257594.wav")
fackelsound = pygame.mixer.Sound(r"Main\sounds\breath-264957-1.wav")
bubble_pop = pygame.mixer.Sound(r"Main\sounds\bubble-pop-293342-_1_.wav")
sword_slice= pygame.mixer.Sound(r"Main\sounds\sword-slice-393847-_1_.wav")
monkey_noise = pygame.mixer.Sound(r"Main\sounds\monkey-noise-sound-effect-no-copyright-390901-_1_.wav")
walking_main_character = pygame.mixer.Sound(r"Main\sounds\foot-steps-77348-1.wav")
crafting_axe = pygame.mixer.Sound(r"Main\sounds\rock-cinematic-161648.wav")
laser_aus_sound = pygame.mixer.Sound(r"Main\sounds\laser_aus.wav")

channel_background = pygame.mixer.Channel(0) #weist den Sounds verschiedene Channels zu, damit sie gleichzeitig abgespielt werden können
channel_water = pygame.mixer.Channel(1)
channel_breath = pygame.mixer.Channel(2)
channel_bubble_pop = pygame.mixer.Channel(3)
channel_sword = pygame.mixer.Channel(4)
channel_monkey = pygame.mixer.Channel(5)
channel_walk = pygame.mixer.Channel(6)
channel_crafting_axe = pygame.mixer.Channel(7)
channel_fackelsound = pygame.mixer.Channel(8)
channel_laser_aus = pygame.mixer.Channel(9)

def play_background_music(): #Hintergrundmusik (IMPLEMENTIERT)
    channel_background.play(slow_theme, loops = -1)

def play_pilz_abbauen(): #beim abauen der Pilzes (x)
    channel_water.set_volume(0.1)
    channel_water.play(pilz_abbauen)

def play_fackelsound(): #Sound, sobald man eine Fackel in der Hand hält (x)
    channel_fackelsound.set_volume(0.1)
    channel_fackelsound.play(fackelsound)

def play_bubble_pop(): #Sound für das aufsammeln von Items (IMPLEMENTIERT)
    channel_bubble_pop.set_volume(0.9)
    channel_bubble_pop.play(bubble_pop)
    print("bubble_pop")

def play_sword_slice(): #beim angreifen eines Mobs (x)
    channel_sword.set_volume(0.1)
    channel_sword.play(sword_slice)

def play_monkey_noise(): #Endanimation (x)
    channel_monkey.set_volume(0.1)
    channel_monkey.play(monkey_noise)

def play_walking_main_character(): #Laufsound des Hauptcharakters (IMPLEMENTIERT)
    channel_walk.set_volume(0.1)
    channel_walk.play(walking_main_character)

def stop_walking_main_character():
    channel_walk.stop()

def play_crafting_axe(): #Sound für das craften der Axt (IMPLEMENTIERT)
    channel_crafting_axe.set_volume(0.1)
    channel_crafting_axe.play(crafting_axe)
    print("crafting_axe")

def laser_aus(): #Sound, soblad der Laser ausgeschaltet wird ()
    channel_laser_aus.set_volume(0.6)
    channel_laser_aus.play(laser_aus_sound)
    print("laser_aus")