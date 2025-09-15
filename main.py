import pygame
import Main.settings as settings
import Engine.entities as entities
import Main.events as events
import Player.player as player
import sys
import time



pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])

clock = pygame.time.Clock()

entities_group = pygame.sprite.Group()  
moving_entities_group = pygame.sprite.Group()
playerGroup = pygame.sprite.GroupSingle()

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (64,64), r"pixilart-sprite.png",True, True, True, 0, 10, {"walking_w": [0, 1, 20, True], "walking_s": [2, 3, 20, True], "walking": [4, 5, 20, True]})
Wall = entities.Entity(250, 250, pygame.Rect(0, 0, 64, 64), "midbottom", (64,64), r"Wall.png", True, False)

entities_group.add(Wall)
playerGroup.add(Player)
        
Colliton = events.Collision(entities_group, moving_entities_group)


# Run until the user asks to quit

a = True

running = True
while running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    Colliton.update()

    screen.fill((255, 255, 255))

    entities_group.update(-Player.dx, -Player.dy, keys)
    entities_group.draw(screen)

    moving_entities_group.update(-Player.dx, -Player.dy, keys,)
    moving_entities_group.draw(screen)

    playerGroup.update(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, keys)
    playerGroup.draw(screen)

    
    pygame.display.update()
    clock.tick(60)


pygame.quit()