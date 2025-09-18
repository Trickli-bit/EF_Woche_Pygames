import pygame
import Main.settings as settings
import Engine.entities as entities
import Main.events as events
import Player.player as player
import Main.generation as generation
import Engine.Entity_Classes.floor as Floor
import Engine.Entity_Classes.interactable as interactable
import Engine.Entity_Classes.inventorySlot as inventory
import sys
import time
import Engine.Entity_Classes.collectable as collectable
import Main.sounds as sounds
import Engine.Entity_Classes.npc as npc
import Engine.Entity_Classes.animations as animations


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
vignietteSmall = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), "center", (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), r"Vigniette2.png",False, False, False, 0, 0, {})

Player = player.Player(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 64, 64), "midbottom", (80, 80), r"Player\player.png",True, True, True, 13, 21, {"walking_a": [0, 3, 5, True], "walking_d": [5, 8, 5, True], "walking_s": [10, 15, 5, True], "walking_w": [17, 19, 5, True]})
Axecrafter = interactable.interactables(2200,1600, pygame.Rect(0, 0, 64, 64), "topleft", (128,128), r"Engine\Entity_Classes\Sprites_Entity_Classes\pixilart-sprite (6).png", True, True, "Axe", "Stick", "Rock", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 10, False]}, "Craft_Axe")
StartAnimation = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 448, 256), "center", (886, 512), r"StartAnimation.png", False, True, False, 0, 14, {"Start": [1, 13, 10, False]} )
EndAnimation = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 256, 144), "center", (1024, 576), r"EndAnimation.png", False, True, False, 0, 65, {"End": [0, 64, 10, False]} )
PoI = entities.Entity(settings.SCREEN_HEIGHT//2 + 50, settings.SCREEN_WIDTH//2 + 50, pygame.Rect(0,0, 64, 64), "center", (64, 64), r"Main\PoI.png", False, True, False, 0, 3, {"PoI": [0, 2, 10, True]})
start_animation_counter = 0
Turtle = npc.Turtle(2400, 1800, width_blocks=4, height_blocks=4)
RecipeBook = collectable.RecipeBook(Axecrafter.pos_x+32, Axecrafter.pos_y+32)
StartText = entities.Entity(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, pygame.Rect(0, 0, 448, 256), "center", (886, 512), r"Start_text.png", False, True, False, 0, 8, {"Start": [0, 3, 50, False], "Explanation": [4, 7, 350, False]} )
trigger = None

overlayGroup_2.add(vigniette, PoI)

playerGroup.add(Player)
                
entities_group.add(Axecrafter, RecipeBook, Turtle)

animationGroup.add(StartAnimation)

Collition = events.Collision(entities_group, moving_entities_group, playerGroup)

# Run until the user asks to quit

addable = True
maingame = False
start_generation = False
start_startanimation = True 
start_introduction_animation = False
introduction_go = False
game_finished = False
waiting_on_start_button = True
end_animation_started = False
end_counter = 0


cooldown = 6
Vignette = True
BigMap = False
Recipe = False

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

        if start_introduction_animation:
            start_animation_counter += 1
            animationGroup.add(StartText)
            StartText.Animation.start_animation("Start")
            start_introduction_animation = False
        
        if start_animation_counter == 1400 or (keys[pygame.K_ESCAPE] and start_animation_counter >= 10):
            if not waiting_on_start_button: 
                start_animation_counter = 0
                StartText.Animation.stop_animation(7)
                start_startanimation = False
                start_generation = True
                maingame = True  

        if keys[pygame.K_ESCAPE] and waiting_on_start_button:
            sounds.play_start_animation()
            keys = []
            waiting_on_start_button = False
            StartAnimation.Animation.start_animation("Start")
            StartAnimation.base_sprite = 8

        if not waiting_on_start_button:    
            start_animation_counter += 1
        
        if start_animation_counter == 130:
            start_introduction_animation = True
            animationGroup.remove(StartAnimation)
            

        if start_animation_counter == 280:
            StartText.Animation.stop_animation(3)
            StartText.Animation.start_animation("Explanation")





    if start_generation:
        sounds.channel_start_animation.stop()
        Map = generation.generateLandscape(floor_group, entities_group, trigger)
        Map.generateGrass()
        trigger = Map.generateItems()
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
            if isinstance(addable, animations.pick_up_animation):
                addable.Animation.start_animation("pick_up")
            if isinstance(addable, animations.interact_animation):
                addable.Animation.start_animation("interaction")
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
        
        if Vignette == True:
            if generation.GetNumberOfItems("Torch") == 0:
                sounds.play_fackelsound()
                overlayGroup_2.remove(vigniette)
                overlayGroup_2.add(vignietteSmall)
                Vignette = False
                BigMap = False
                Recipe = False 
        
        if BigMap == False:
            if generation.GetNumberOfItems("Map") == 0:
                overlayGroup_2.add(inventory.InventorySlot(0, settings.SCREEN_HEIGHT - 180.9, pygame.Rect(0, 0, 794, 603), (238.2, 180.9), r"Engine\Entity_Classes\Sprites_Entity_Classes\MapBig.png"))
                BigMap = True

        if Recipe == False:
            if generation.GetNumberOfItems("RecipeBook") == 0:
                overlayGroup_2.add(inventory.InventorySlot(18, 0, pygame.Rect(0, 0, 64, 64), (192, 192), r"Engine\Entity_Classes\Sprites_Entity_Classes\Recipe.png"))
                Recipe = True

        entities_group.update(-Player.dx, -Player.dy, keys)
        entities_group.draw(screen)

        moving_entities_group.update(-Player.dx, -Player.dy, keys)
        moving_entities_group.draw(screen)

        animationGroup.update(-Player.dx, -Player.dy, keys)
        animationGroup.draw(screen)

        trigger.x += -Player.dx
        trigger.y += -Player.dy

        playerGroup.update(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2, keys)
        playerGroup.draw(screen)

        overlayGroup_2.draw(screen)
        Collition.update()
        
        overlayGroup.update(-Player.dx, -Player.dy, keys,)
        overlayGroup.draw(screen)

        overlayGroup = generation.updateInventory()

        if trigger is not None:
            print(trigger)
            if trigger.colliderect(Player.rect):
                game_finished = True

        

    if game_finished:
        trigger = None
        sounds.stop_all_sounds()
        sounds.play_finale()
        animationGroup.add(EndAnimation)
        game_finished = False
        maingame = False
        end_animation_started = True
        EndAnimation.Animation.start_animation("End")
    if end_animation_started:
        screen.fill((0,0,0))
        animationGroup.update()
        animationGroup.draw(screen)
        end_counter += 1
        if end_counter == 480:
            sounds.play_monkey_noise()
        if EndAnimation.Animation.active == False:
            time.sleep(5)
            end_animation_started = False
            animationGroup.remove(EndAnimation)
            Player.dx = 0
            Player.dy = 0
            Axecrafter.has_tool = False
            start_startanimation = True
            running = False


    if game_finished:
        sounds.stop_background_music()
        print("finished")
        animationGroup.add(EndAnimation)
        game_finished = False
        maingame = False
        end_animation_started = True
        EndAnimation.Animation.start_animation("End")



    pygame.display.update()
    clock.tick(60)

pygame.quit()

#cx 52