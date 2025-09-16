import Engine.entities as entities
import pygame

class Floor(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

class Grass(Floor):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Floor.png", solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={}, flip = (False, False)):
        self.base_sprite = base_sprite
        
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, 6, ani_animations)

        

        if not hasattr(self, "image") or self.image is None:
            print("WARNUNG: Kein Bild für Grass!")

        if flip is not (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])

    def update(self, dx = 0, dy = 0, keys = []):
        super().update(dx, dy, keys)
