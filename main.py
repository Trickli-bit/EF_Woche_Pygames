import pygame
import Main.settings as settings
import Engine.entities as entities
import Main.events as events
import Player.player as player
import Main.generation as generation
import Engine.Entity_Classes.floor as Floor
import Engine.Entity_Classes.interactable as interactable
import sys
import time
import Engine.Entity_Classes.collectable as collectable
import Main.sounds as sounds


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])

clock = pygame.time.Clock()

entities_group = pygame.sprite.Group()  
floor_group = pygame.sprite.Group()
moving_entities_group = pygame.sprite.Group()
playerGroup = pygame.sprite.GroupSingle()
overlayGroup = pygame.sprite.Group()
animationGroup = pygame.sprite.Group()
overlayGroup_2= pygame.sprite.Group()

vigniette = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), "center", (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), r"vigniette.png",False, False, False, 0, 0, {})

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (64, 64), r"Player\player.png",True, True, True, 0, 17, {"walking_a": [0, 3, 5, True], "walking_d": [4, 7, 5, True], "walking_s": [8, 13, 5, True], "walking_w": [14, 16, 5, True]})
Axecrafter = interactable.interactables(0, 0, pygame.Rect(0, 0, 64, 64), "topleft", (64,64), r"Engine\Entity_Classes\Sprites_Entity_Classes\pixilart-sprite (6).png", True, True, "Axe", "Stick", "Rock", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 5, False]}, "Craft_Axe")

Stick = collectable.Stick(100, 50)  # Erstelle ein Stick-Objekt an Position (300, 700), muss noch mit der Generation verbunden werden
Rock = collectable.Rock(100, 150)
Mushroom_juice = collectable.Mushroom_juice(100, 250)

entities_group.add(Stick)  # Füge das Stick-Objekt zur Entitäten-Gruppe hinzu, damit es im Spiel erscheint
entities_group.add(Rock)
entities_group.add(Mushroom_juice)

overlayGroup_2.add(vigniette)
entities_group.add(Axecrafter)
playerGroup.add(Player)

        


Collition = events.Collision(entities_group, moving_entities_group, playerGroup)

# Run until the user asks to quit

addable = True
start_generation = True

print("GOOOOO")

running = True
while running:

    screen.fill((255, 255, 255))

    Stick.collide_with_player(Player)
    Rock.collide_with_player(Player)
    Mushroom_juice.collide_with_player(Player)


    if start_generation:
        Map = generation.generateLandscape(floor_group, entities_group)
        Map.generateGrass()
        Map.generateWall()
        sounds.play_background_music()
        start_generation = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()


    floor_group.update(-Player.dx, -Player.dy, keys)
    floor_group.draw(screen)

    addable = events.addingAnimation()
    if addable is not None:
        animationGroup.add(addable)
        addable.Animation.start_animation("pick_up")
        events.animation_to_add = None
        addable = None

    for anim in animationGroup.sprites():
        # Wenn eine Animation existiert und inactive ist, entferne das Sprite
        if hasattr(anim, "Animation") and anim.Animation.active == False:
            # Hier kill() um sicher aus allen Gruppen entfernt zu werden
            anim.kill()


    entities_group.update(-Player.dx, -Player.dy, keys)
    entities_group.draw(screen)

    moving_entities_group.update(-Player.dx, -Player.dy, keys)
    moving_entities_group.draw(screen)

    animationGroup.update(-Player.dx, -Player.dy, keys)
    animationGroup.draw(screen)

    playerGroup.update(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, keys)
    playerGroup.draw(screen)

    overlayGroup_2.draw(screen)

    Collition.update()
    
    overlayGroup.update(-Player.dx, -Player.dy, keys,)
    overlayGroup.draw(screen)

    overlayGroup = generation.updateToolbar()


    if Player.rect.colliderect(Axecrafter.rect) and Axecrafter.has_tool == False:
        Axecrafter.interact()

    pygame.display.update()
    clock.tick(60)


pygame.quit()