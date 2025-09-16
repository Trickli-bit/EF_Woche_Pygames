import pygame
import Main.settings as settings
import Engine.entities as entities
import Main.events as events
import Player.player as player
import sys
import time
import Engine.Entity_Classes.collectable as collectable


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])

clock = pygame.time.Clock()

entities_group = pygame.sprite.Group()  
moving_entities_group = pygame.sprite.Group()

Bob = player.Player(500, 250, pygame.Rect(0, 0, 64, 64), "midbottom", (64,64), r"pixilart-sprite.png",True, True, 0, 10, {"walking_w": [0, 1, 20, True], "walking_s": [2, 3, 20, True], "walking": [4, 5, 20, True]})
Wall = entities.Entity(250, 250, pygame.Rect(0, 0, 64, 64), "midbottom", (64,64), r"Wall.png", True, False)
#Stick = entities.Entity(300, 250, pygame.Rect(0, 0, 64, 64), "midbottom", (64,64), r"Stick.png", False, False)
Stick2 = collectable.Stick(200, 250)
entities_group.add(Wall)
entities_group.add(Stick2)
moving_entities_group.add(Bob)
        



# Run until the user asks to quitw

a = True

running = True
while running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()


    screen.fill((255, 255, 255))

    entities_group.update(keys)
    entities_group.draw(screen)

    moving_entities_group.update(keys)
    moving_entities_group.draw(screen)

    for collect in [e for e in entities_group if isinstance(e, collectable.Collectable)]:
        if Bob.rect.colliderect(collect.rect):
            collect.collide_with_collectable(Bob)

    pygame.display.update()
    clock.tick(60)


pygame.quit()