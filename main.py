import pygame
import entities
import settings
import sys
import sprite_sheet
import time


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])

clock = pygame.time.Clock()

entities_group = pygame.sprite.Group()  

Bob = entities.EntityMovable(250, 250, pygame.Rect(0, 0, 64, 64), "midbottom", (64,64), r"pixilart-sprite.png", True, 0, 10, {"walking_w": [0, 1, 20, True], "walking_s": [2, 3, 20, True], "walking": [4, 5, 20, True]})

entities_group.add(Bob)
    
        


# Run until the user asks to quit

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

    
    pygame.display.update()
    clock.tick(60)


pygame.quit()