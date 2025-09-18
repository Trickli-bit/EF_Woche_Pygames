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
import Engine.Entity_Classes.npc as npc


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

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (96, 96), r"Player\player.png",True, True, True, 13, 21, {"walking_a": [0, 3, 5, True], "walking_d": [5, 8, 5, True], "walking_s": [10, 15, 5, True], "walking_w": [17, 19, 5, True]})
Axecrafter = interactable.interactables(2200,1600, pygame.Rect(0, 0, 64, 64), "topleft", (128,128), r"Engine\Entity_Classes\Sprites_Entity_Classes\pixilart-sprite (6).png", True, True, "Axe", "Stick", "Rock", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 10, False]}, "Craft_Axe")
StartAnimation = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 450, 256), "center", (900, 512), r"StartAnimation.png", False, True, False, 0, 14, {"Start": [1, 13, 10, False]} )
PoI = entities.Entity(settings.SCREEN_HEIGHT//2 + 50, settings.SCREEN_WIDTH//2 + 50, pygame.Rect(0,0, 64, 64), "center", (64, 64), r"Main\PoI.png", False, True, False, 0, 3, {"PoI": [0, 2, 10, True]})
start_animation_counter = 0
Turtle = npc.Turtle(2400, 1800, width_blocks=4, height_blocks=4)



overlayGroup_2.add(vigniette)

#>>>>>>>>> Temporary merge branch 2
playerGroup.add(Player)

animationGroup.add(StartAnimation)

        


Collition = events.Collision(entities_group, moving_entities_group, playerGroup)

# Run until the user asks to quit

addable = True
maingame = False
start_generation = False
start_startanimation = True 

cooldown = 6

running = True
while running:

    

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    screen.fill((255, 255, 255))


    if start_startanimation:
        screen.fill((0,0,0))
        start_generation = False
        animationGroup.update()
        animationGroup.draw(screen)
        start_animation_counter += 1
        if start_animation_counter == 300:
            StartAnimation.Animation.start_animation("Start")
            StartAnimation.base_sprite = 8
        
        if start_animation_counter == 430:
            start_animation_counter = 0
            animationGroup.remove(StartAnimation)
            start_startanimation = False
            start_generation = True
            maingame = True
            
        
        


    if start_generation:
        Map = generation.generateLandscape(floor_group, entities_group)
        Map.generateGrass()
        Map.generateItems()
        Map.generateWall()
        Map.generatePrices()
        Player.dx = settings.MIDDLE_X
        Player.dy = settings.MIDDLE_Y

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

        if keys[pygame.K_q]:
            cooldown -= 1
            if cooldown <= 0 and len(generation.itemField_group) > 0:
                entities_group.add(generation.dropItemFromInventory())
                cooldown = 6
                
            print("ITEMFIELD_GROUP", generation.itemField_group, cooldown > 0 and len(generation.inventoryCollectables) > 0)

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

        overlayGroup = generation.updateInventory()

        if Player.rect.colliderect(Axecrafter.rect) and Axecrafter.has_tool == False:
            sounds.play_crafting_axe()
            Axecrafter.interact()

    pygame.display.update()
    clock.tick(60)


pygame.quit()