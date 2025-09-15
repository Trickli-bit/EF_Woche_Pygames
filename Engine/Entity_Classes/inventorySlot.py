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