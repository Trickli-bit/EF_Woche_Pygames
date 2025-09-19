import Engine.entities as entities
import pygame

class Floor(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid=False, is_spritesheet=True, fix=False, base_sprite=0, ani_frames_count=5, ani_animations={}):
        """
        A floor entity in the game world.
        Inherits from entities.Entity and represents any solid or non-solid floor surface.
        Handles sprite animations if a spritesheet is provided.
        """
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)


class Grass(Floor):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0, 0, 64, 64), rect_attach="topleft", scale=(64, 64),
                 source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Floor.png", solid=False, is_spritesheet=True,
                 fix=False, base_sprite=0, ani_frames_count=5, ani_animations={}, flip=(False, False)):
        """
        A specific type of Floor entity representing grass.

        Adds optional sprite flipping and sets a default grass texture.
        """
        self.base_sprite = base_sprite

        # Calls Floor constructor, but forces ani_frames_count = 6 for grass
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, 6, ani_animations)

        # Flips the sprite if flip is enabled
        if flip != (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])

    def update(self, dx=0, dy=0, keys=[]):
        """
        Updates the grass entity state.
        """
        super().update(dx, dy, keys)
