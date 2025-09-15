import pygame
import Main.settings as settings
import Engine.entities as entities
import Main.events as events
import Player.player as player
import Main.generation as generation
import Engine.Entity_Classes.floor as Floor 
import sys
import time



pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])

clock = pygame.time.Clock()

entities_group = pygame.sprite.Group()  
floor_group = pygame.sprite.Group()
moving_entities_group = pygame.sprite.Group()
playerGroup = pygame.sprite.GroupSingle()

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (64, 64), r"Player\player.png",True, True, True, 0, 17, {"walking_a": [0, 3, 5, True], "walking_d": [4, 7, 5, True], "walking_s": [8, 13, 5, True], "walking_w": [14, 16, 5, True]})



entities_group.add()
playerGroup.add(Player)
        
Colliton = events.Collision(entities_group, moving_entities_group)

# Run until the user asks to quit

a = True
start_generation = True

print("GOOOOO")

running = True
while running:

    screen.fill((255, 255, 255))

    if start_generation:
        Map = generation.generateLandscape(floor_group)
        Map.generateElements()
        start_generation = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    Colliton.update()

    floor_group.update(-Player.dx, -Player.dy, keys)
    floor_group.draw(screen)

    entities_group.update(-Player.dx, -Player.dy, keys)
    entities_group.draw(screen)

    moving_entities_group.update(-Player.dx, -Player.dy, keys,)
    moving_entities_group.draw(screen)

    playerGroup.update(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, keys)
    playerGroup.draw(screen)

    
    pygame.display.update()
    clock.tick(60)


pygame.quit()