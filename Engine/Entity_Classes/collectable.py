import Engine.entities as entities
import Main.events
import Main.generation as generation
import pygame
import Player.player as player

class Collectable(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale = (64,64), source = None, solid = False, is_spritesheet = False, base_sprite = 0, ani_frames_count = 0, ani_animations = {}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)

        self.name = "Collectable"  # Basisname
        self.value = 0
        self.collected = False  # Ob das Objekt schon gesammelt wurde
    

    def collide_with_player(self, player_obj):
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
            self.kill()  # Entfernt das Collectable aus allen Sprite-Gruppen
            return generation.addItemToInventory(self)

class Stick(Collectable):
     def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64,64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\stock-pixilart (2).png", solid = False, is_spritesheet = False, base_sprite=0, ani_frames_count=0, ani_animations= {}):
          super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
          
          self.name = "Stick"
          self.value = 1
        

class Rock(Collectable):
        def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64,64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\stein-pixilart (5).png", solid = False, is_spritesheet = False, base_sprite=0, ani_frames_count=0, ani_animations= {}):
            super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
            
            self.name = "Rock"
            self.value = 1
        