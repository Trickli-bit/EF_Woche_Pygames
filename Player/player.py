import pygame
from Engine.entities import EntityMovable
import Main.sounds as sounds
import Engine.Entity_Classes.interactable as interactable
import Engine.Entity_Classes.npc as npc
import Main.inventoryManager as inventory
import Engine.Entity_Classes.animations as animations
import Main.events as events

class Player(EntityMovable):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix = False, base_sprite=0, ani_frames_count=0, ani_animations=...):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        
        # Inventar als Attribut speichern
        self.name = "Player"  # optional, gut für Debug
        self.item_dict = {"Stick": 0, "Rock": 0, "Mushroom_juice": 0} #muss speter mit dem Inventar von Aiko abgeglichen werden!!!
        self.animations = ani_animations or {}
        self.ready_to_attack = False
        self.attaking_objects = []
        self.kill_go = False
        self.is_moving = False
        self.wall_group = None

        # Kollisions-Box Offset und Größe separat definieren
        self.collision_offset_x = 10
        self.collision_offset_y = 20
        self.collision_width = 64
        self.collision_height = 64

        # Trigger-Collision-Rect initialisieren
        self.trigger_collition = pygame.Rect(
            self.rect.x + self.collision_offset_x,
            self.rect.y + self.collision_offset_y,
            self.collision_width,
            self.collision_height)


    def get_Wall_group(self, group):
        self.Wall_group = group


    def checkcollition(self):
        print(self.Wall_group)
        for element in self.Wall_group:        
             if element.rect.colliderect(self.trigger_collition):
                 print("Collition")
                 return True
        return False
    

    def calculating_movement(self, keys):

        """ Berechnet die Bewegung basierend auf den gedrückten Tasten.
        param:\t keys (pygame.key.get_pressed()) """

        collition_check = 0

        self.dx = self.dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx += self.speed
        if keys[pygame.K_SPACE]:
            self.interact = animations.interact_animation(self.rect.centerx, self.rect.centery)
            events.checkAnimations(self.interact)
            self.attack()

        self.trigger_dx = self.dx
        self.trigger_dy = self.dy
    



        # Diagonalbewegung anpassen (optional, für gleichmäßige Geschwindigkeit)
        if self.dx != 0 and self.dy != 0:
            self.dx = int(self.dx / 1.4142)
            self.dy = int(self.dy / 1.4142)

        moving_now = self.dx != 0 or self.dy != 0

        self.trigger_collition.x += self.dx * 4
        self.trigger_collition.y += self.dy * 4

        print(self.dx)

        print(self.trigger_collition.x, self.trigger_collition.y, self.rect.x, self.rect.y)

        print(self.checkcollition())

        if not self.checkcollition():


            # Laufsound nur starten, wenn Bewegung beginnt
            if moving_now and not self.is_moving:
                sounds.play_walking_main_character()
            # Laufsound stoppen, wenn Bewegung endet
            elif not moving_now and self.is_moving:
                sounds.stop_walking_main_character()

            # Flag aktualisieren <-----------
            self.is_moving = moving_now


            #if self.dx != 0 or self.dy != 0:
                #sounds.play_walking_main_character()

            #if not (self.dx != 0 or self.dy != 0):
                #sounds.stop_walking_main_character()

        else:
            self.is_moving = False
            self.dx = 0
            self.dy = 0
        self.trigger_collition.x -= self.trigger_dx * 4
        self.trigger_collition.y -= self.trigger_dy * 4

    def attack(self):
        if self.ready_to_attack and sum(1 for elem in inventory.inventoryCollectables if elem.function == "Item") < 7:
            for entity in self.attaking_objects:
                if isinstance(entity, interactable.Mushroom):
                    if inventory.GetNumberOfItems("Axe") == 0:
                        self.kill_go = True
                    if self.kill_go:
                        entity.die(has_axe=True)
                        self.ready_to_attack = False
                        self.attaking_objects = []
                        self.kill_go = False
                        break  # Nach dem ersten Kill abbrechen
                elif isinstance(entity, npc.Turtle):
                    if inventory.GetNumberOfItems("Torch") == 0:
                        self.kill_go = True
                    if self.kill_go:
                        entity.die()
                        self.ready_to_attack = False
                        self.attaking_objects = []
                        self.kill_go = False
                        break
        


    def update(self, dx = 0, dy = 0, keys = None):

        self.trigger_collition.x = self.rect.x + self.collision_offset_x
        self.trigger_collition.y = self.rect.y + self.collision_offset_y

        """ Aktualisiert die Position und Animation des Spielers.
        param:\t keys (pygame.key.get_pressed()) """
        if keys is None:
            keys = []

        # 1) Berechne die Bewegung basierend auf Tastendrücken -> setzt self.dx / self.dy
        if keys:
            self.calculating_movement(keys)

        # 2) Trigger Animation basierend auf self.dx / self.dy (direkt, damit Animation korrekt gesetzt wird)
        #    (ruft die Methode aus EntityMovable, die jetzt robuster mit Flip umgeht)
        self.animation_movement_adjustement()

        # 3) Danach das normale Update von Entity/EntityMovable ausführen.
        #    Wichtig: wir übergeben die Parameter dx,dy wie vom main-loop erwartet
        super().update(dx, dy, keys)

    
