import pygame
import Main.settings as settings
import Engine.entities as entities
import Main.events as events
import Player.player as player
import Main.generation as generation
import Engine.Entity_Classes.floor as Floor 
import sys
import time
import Engine.Entity_Classes.collectable as collectable


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])

clock = pygame.time.Clock()

entities_group = pygame.sprite.Group()  
floor_group = pygame.sprite.Group()
moving_entities_group = pygame.sprite.Group()
playerGroup = pygame.sprite.GroupSingle()
overlayGroup = pygame.sprite.Group()

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (64, 64), r"Player\player.png",True, True, True, 0, 21, {"walking_a": [0, 3, 5, True], "walking_d": [5, 8, 5, True], "walking_s": [10, 15, 5, True], "walking_w": [17, 19, 5, True]})

Stick = collectable.Stick(50, 50)  # Erstelle ein Stick-Objekt an Position (300, 700), muss noch mit der Generation verbunden werden
Rock = collectable.Rock(100, 100)

entities_group.add(Stick)  # Füge das Stick-Objekt zur Entitäten-Gruppe hinzu, damit es im Spiel erscheint
entities_group.add(Rock)

playerGroup.add(Player)

        
Colliton = events.Collision(entities_group, moving_entities_group, playerGroup)

# Run until the user asks to quit

a = True
start_generation = True

running = True
while running:

    screen.fill((255, 255, 255))

    new_overlay = Stick.collide_with_player(Player)
    if new_overlay:
        overlayGroup = new_overlay

    new_overlay = Rock.collide_with_player(Player)
    if new_overlay:
        overlayGroup = new_overlay

    if start_generation:
        Map = generation.generateLandscape(floor_group, entities_group)
        Map.generateGrass()
        Map.generateWall()
        start_generation = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    floor_group.update(-Player.dx, -Player.dy, keys)
    floor_group.draw(screen)

    entities_group.update(-Player.dx, -Player.dy, keys)
    entities_group.draw(screen)

    moving_entities_group.update(-Player.dx, -Player.dy, keys)
    moving_entities_group.draw(screen)

    playerGroup.update(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, keys)
    playerGroup.draw(screen)

    Colliton.update()
    overlayGroup.update(-Player.dx, -Player.dy, keys,)
    overlayGroup.draw(screen)

    pygame.display.update()
    clock.tick(60)


pygame.quit()