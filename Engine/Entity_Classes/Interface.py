import pygame
import Engine.entities as entities

class Interface(entities.Entity):
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


class PriceInventorySlot(entities.Entity):
    """Klasse, die ein Inventory Slot als Entity definiert. \tpos_x: float für X-Position, \tpos_x: float für Y-Position, \trect: pygame.Rect für Xpos/Ypos/Höhe/Breite, \t scale: Tupel für Breite/Höhe, \tsource: String für Dateipfad"""
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\InventorySlot_Price.png", solid = False, is_spritesheet = False , fix=False, base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
      
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.near_items = []

    def update_image(self):
        """Funktion, die das Bild neu lädt basierend auf self.source und self.scale."""
        self.image = pygame.transform.scale(pygame.image.load(self.source), self.scale)