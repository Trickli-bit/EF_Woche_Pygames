import Engine.entities as entities
import Main.events
import Main.generation as generation
import pygame
import Player.player as player
import Engine.Entity_Classes.animations as animations 
import Main.events as events
import Main.sounds as sounds

# collectable.py (relevanter Ausschnitt)
class Collectable(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach,
                 scale=(64,64), source=None, solid=False, is_spritesheet=False,
                 fix=False, base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.value = 0
        self.collected = False
        self.pick_up = None
        self.source = source
        self.function = "Item"
        self.should_pick_up = True
        print("getting created")


    def collide_with_player(self, player_obj):
        if self.should_pick_up:
            """
            Prüft, ob der Spieler das Collectable berührt.
            Nur wenn die Rechtecke überlappen und das Objekt noch nicht gesammelt wurde.
            """
            if self.collected:
                pass
                return  # Schon gesammelt, nichts tun

            if not isinstance(player_obj, player.Player):
                pass
                #return  # Nur Player kann sammeln

            # Kollisionsprüfung mit Rechtecken
            if self.rect.colliderect(player_obj.rect):
                print("COLLITION")
                self.collected = True
                player_obj.item_dict[self.name] = player_obj.item_dict.get(self.name, 0) + self.value
                print(f"[DEBUG] {player_obj} hat {self.name} eingesammelt! Inventar: {player_obj.item_dict}")
                self.pick_up = animations.pick_up_animation(self.rect.centerx, self.rect.centery)
                events.checkAnimations(self.pick_up)
                


                sounds.play_bubble_pop()
                self.kill()  # Entfernt das Collectable aus allen Sprite-Gruppen
                return generation.addItemToInventory(self)
        
    def zur_gruppe_hinzufuegen(self, gruppe):
            gruppe.add(self)

    def update(self, dx = 0, dy = 0, keys = []):
        super().update(dx, dy, keys)
        

         


class Stick(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\stock-pixilart (2).png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Stick"
        self.function = "Item"
        self.value = 1

class Rock(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\stein-pixilart (5).png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Rock"
        self.function = "Item"
        self.value = 1

class Mushroom_juice(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\mushroo_juice.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Mushroom_juice"
        self.function = "Item"
        self.value = 1   

class Axe(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Axe.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Axe"
        self.function = "Tool"
        self.value = 1
