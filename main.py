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

Bob = entities.Entity(500, 500, 64, 64, "center", (64,64), r"C:\Users\timon\OneDrive\Documents\Lerbermatt\GYM3\EF Info\Pygames\db6hy2w-4db8a954-a6e1-4e46-b202-2d2786241df4 (1).png", True, 0, 10, {"laufen": [0, 5, 20], "rennen": [6,10,10]})

entities_group.add(Bob)
    
        


# Run until the user asks to quit

a = True

running = True
while running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        Bob.Animation.start_animation("laufen")



    screen.fill((255, 255, 255))

    entities_group.update()
    entities_group.draw(screen)

    
    pygame.display.update()
    clock.tick(60)


pygame.quit()