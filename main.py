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

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (64, 64), r"Player\player.png",True, True, True, 0, 21, {"walking_a": [0, 3, 5, True], "walking_d": [5, 8, 5, True], "walking_s": [10, 15, 5, True], "walking_w": [17, 19, 5, True]})
StartAnimation = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 256, 256), "center", (512, 512), r"StartAnimation.png", False, True, False, 0, 10, {"Start": [1, 9, 10, False]} )
start_animation_counter = 0

Stick = collectable.Stick(100, 50)  # Erstelle ein Stick-Objekt an Position (300, 700), muss noch mit der Generation verbunden werden
Rock = collectable.Rock(100, 150)
Mushroom_juice = collectable.Mushroom_juice(100, 250)

entities_group.add(Stick)  # Füge das Stick-Objekt zur Entitäten-Gruppe hinzu, damit es im Spiel erscheint
entities_group.add(Rock)
entities_group.add(Mushroom_juice)

overlayGroup_2.add(vigniette)
playerGroup.add(Player)

animationGroup.add(StartAnimation)

        


Collition = events.Collision(entities_group, moving_entities_group, playerGroup)

# Run until the user asks to quit

addable = True
maingame = False
start_generation = False
start_startanimation = True 

running = True
while running:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    screen.fill((255, 255, 255))

    new_overlay = Stick.collide_with_player(Player)
    if new_overlay:
        overlayGroup = new_overlay

    new_overlay = Rock.collide_with_player(Player)
    if new_overlay:
        overlayGroup = new_overlay

    new_overlay = Mushroom_juice.collide_with_player(Player)
    if new_overlay:
        overlayGroup = new_overlay

    if start_startanimation:
        screen.fill((0,0,0))
        print(start_animation_counter)
        start_generation = False
        animationGroup.update()
        animationGroup.draw(screen)
        start_animation_counter += 1
        if start_animation_counter == 300:
            StartAnimation.Animation.start_animation("Start")
            StartAnimation.base_sprite = 8
        if start_animation_counter == 400:
            start_animation_counter = 0
            start_startanimation = False
            start_generation = True
            maingame = True
        
        


    if start_generation:
        Map = generation.generateLandscape(floor_group, entities_group)
        Map.generateGrass()
        Map.generateWall()
        sounds.play_background_music()
        start_generation = False

    if maingame:



        floor_group.update(-Player.dx, -Player.dy, keys)
        floor_group.draw(screen)

        addable = events.addingAnimation()
        if addable is not None:
            animationGroup.add(addable)
            addable.Animation.start_animation("pick_up")
            events.animation_to_add = None
            addable = None

        for anim in animationGroup.sprites():
            if hasattr(anim, "Animation") and anim.Animation.active == False:
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

    pygame.display.update()
    clock.tick(60)


pygame.quit()