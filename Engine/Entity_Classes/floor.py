import Engine.entities as entities
import pygame

class Floor(entities.Entity):
    """ Basisklasse für Bodenfliesen.
    Parameter: pos_x (float): x-Position der
    Animation, pos_y (float): y-Position der Animation, rect (pygame.Rect): Rechteck für die Animation, rect_attach (str): Befestigungspunkt des Rechtecks, scale (tuple): Skalierung der Animation, source (str): Pfad zur Bildquelle, solid (bool): Ob die Animation solide ist, is_spritesheet (bool): Ob es sich um ein Sprite-Sheet handelt, fix (bool): Ob die Position fixiert ist, base_sprite (int): Startindex des Sprites, ani_frames_count (int): Anzahl der Animationsframes, ani_animations (dict): Wörterbuch der Animationen.
    """
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
    """
    Aktualisiert die Bodenfliese.
    Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, keys (list): Liste der gedrückten Tasten.
    Rückgabe: Ergebnis der übergeordneten Update-Methode.
    """
class Grass(Floor):
    """ Klasse für Gras-Bodenfliesen.
    Parameter: pos_x (float): x-Position der
    Animation, pos_y (float): y-Position der Animation, rect (pygame.Rect): Rechteck für die Animation, rect_attach (str): Befestigungspunkt des Rechtecks, scale (tuple): Skalierung der Animation, source (str): Pfad zur Bildquelle, solid (bool): Ob die Animation solide ist, is_spritesheet (bool): Ob es sich um ein Sprite-Sheet handelt, fix (bool): Ob die Position fixiert ist, base_sprite (int): Startindex des Sprites, ani_frames_count (int): Anzahl der Animationsframes, ani_animations (dict): Wörterbuch der Animationen.
    """
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Floor.png", solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={}, flip = (False, False)):
        self.base_sprite = base_sprite
    """    Aktualisiert die Gras-Bodenfliese.
    Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, keys (list): Liste der gedrückten Tasten.
    Rückgabe: Ergebnis der übergeordneten Update-Methode.   
    """
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Floor.png", solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={}, flip = (False, False)):
        self.base_sprite = base_sprite
    """    Aktualisiert die Gras-Bodenfliese.
    Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, keys (list): Liste der gedrückten Tasten.
    Rückgabe: Ergebnis der übergeordneten Update-Methode.
    """
    def update(self, dx = 0, dy = 0, keys = []):
        super().update(dx, dy, keys)
    """    Aktualisiert die Gras-Bodenfliese.
    Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, keys (list): Liste der gedrückten Tasten.
    Rückgabe: Ergebnis der übergeordneten Update-Methode.
    """