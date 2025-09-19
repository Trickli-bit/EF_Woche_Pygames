import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(14) #Anzahl der gleichzeitig abspielbaren Sounds
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
break_mushoom = pygame.mixer.Sound(r"Main\sounds\MushroomBreak.mp3")
dying_turtle = pygame.mixer.Sound(r"Main\sounds\TurtleDie.mp3")
start_animation = pygame.mixer.Sound(r"Main\sounds\StartAnimation.mp3")
finale = pygame.mixer.Sound(r"Main\sounds\Finale.mp3")

channel_background = pygame.mixer.Channel(0) #weist den Sounds verschiedene Channels zu, damit sie gleichzeitig abgespielt werden können
channel_water = pygame.mixer.Channel(1)
channel_breath = pygame.mixer.Channel(2)
channel_bubble_pop = pygame.mixer.Channel(3)
channel_sword = pygame.mixer.Channel(4)
channel_monkey = pygame.mixer.Channel(5)
channel_walk = pygame.mixer.Channel(6)
channel_crafting = pygame.mixer.Channel(7)
channel_fackelsound = pygame.mixer.Channel(8)
channel_laser_aus = pygame.mixer.Channel(9)
channel_break_mushroom = pygame.mixer.Channel(10)
channel_kill_turtle = pygame.mixer.Channel(11)
channel_start_animation = pygame.mixer.Channel(12)
channel_finale = pygame.mixer.Channel(13)

"""
Hintergrundmusik (IMPLEMENTIERT)
"""
def play_background_music(): 
    channel_background.set_volume(0.08)
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

def stop_walking_main_character():
    channel_walk.stop()

def play_crafting_axe(): #Sound für das craften der Axt 
    channel_crafting.set_volume(0.9)
    channel_crafting.play(crafting_axe)

"""
Sound für das craften der Fackel (x)
"""
def play_crafting_torche(): 
    channel_crafting.set_volume(0.9)
    channel_crafting.play(crafting_torche, maxtime=2000)

"""
Sound, soblad der Laser ausgeschaltet wird (IMPLEMENTIERT)
"""
def laser_aus(): 
    channel_laser_aus.set_volume(0.6)
    channel_laser_aus.play(laser_aus_sound)

def play_breaking_mushroom():
    channel_break_mushroom.set_volume(0.6)
    channel_break_mushroom.play(break_mushoom)

def play_dying_turtle():
    channel_kill_turtle.set_volume(0.6)
    channel_kill_turtle.play(dying_turtle)

def play_start_animation():
    channel_start_animation.set_volume(0.3)
    channel_start_animation.play(start_animation)

def play_finale():
    channel_finale.set_volume(0.6)
    channel_finale.play(finale)


def stop_all_sounds():
    channel_background.stop()
    channel_water.stop()
    channel_breath.stop()
    channel_bubble_pop.stop()
    channel_sword.stop()
    channel_monkey.stop()
    channel_walk.stop()
    channel_crafting.stop()
    channel_fackelsound.stop()
    channel_laser_aus.stop()
    channel_break_mushroom.stop()
    channel_kill_turtle.stop()