import pygame
from Engine.entities import EntityMovable

class Player(EntityMovable):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite=0, ani_frames_count=0, ani_animations=...):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
        
        # Inventar als Attribut speichern
        self.name = "Player"  # optional, gut für Debug
        self.item_dict = {"Stick": 0, "Rock": 0}

    def calculating_movement(self, keys):
        self.dx = self.dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx += self.speed

        # Diagonalbewegung normalisieren
        if self.dx != 0 and self.dy != 0:
            self.dx = int(self.dx / 1.4142)
            self.dy = int(self.dy / 1.4142)

        self.rect.x += self.dx
        
    def update(self, keys):
        super().update()
        self.calculating_movement(keys)
        self.rect.y += self.dy
