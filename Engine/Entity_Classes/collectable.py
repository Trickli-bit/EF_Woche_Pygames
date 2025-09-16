import Engine.entities as entities
import Main.events
import pygame
import Player.player as player

class Collectable(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale = (64,64), source = None, solid = False, is_spritesheet = False, base_sprite = 0, ani_frames_count = 0, ani_animations = {}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)

        # zusätzliche Collectable-spezifische Werte
        self.name = "Collectable"
        self.value = 0

    
    def collide_with_collectable(self, entity):
        if entity.name == "solid":
            pass
        else:
            self.player.collect_item(entity.name)
            entity.kill()



class Stick(Collectable):
     def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64,64), source = r"pixil-frame-0.png", solid = False, is_spritesheet = False, base_sprite=0, ani_frames_count=0, ani_animations= {}):
          super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
          
          self.name = "Stick"
          self.value = 1
        

class Rock(Collectable):
        def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64,64), source = r"pixil-frame-1.png", solid = False, is_spritesheet = False, base_sprite=0, ani_frames_count=0, ani_animations= {}):
            super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
            
            self.name = "Rock"
            self.value = 1
        