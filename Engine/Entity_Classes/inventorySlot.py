import pygame
import Engine.entities as entities

class InventorySlot(entities.Entity):
    """Klasse, die ein Inventory Slot als Entity definiert. \tpos_x: float für X-Position, \tpos_x: float für Y-Position, \trect: pygame.Rect für Xpos/Ypos/Höhe/Breite, \t scale: Tupel für Breite/Höhe, \tsource: String für Dateipfad"""
    def __init__(self, pos_x, pos_y, rect, scale, source):
        entities.Entity.__init__(self, pos_x, pos_y, rect, "midbottom", scale, source, False, False, True)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = rect
        self.scale = scale
        self.source = source

    def update_image(self):
        """Funktion, die das Bild neu lädt basierend auf self.source und self.scale."""
        self.image = pygame.transform.scale(pygame.image.load(self.source), self.scale)