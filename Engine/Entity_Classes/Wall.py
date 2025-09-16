import Engine.entities as entities
import pygame

class Wall(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Wall.png", solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=7, ani_animations={}, flip = (False, False)):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

        if flip is not (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])