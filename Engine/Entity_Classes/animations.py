import Engine.entities as entities
import pygame

class pick_up_animation(entities.Entity):
    """
    Animation für das Aufsammeln von Items.
    Parameter: pos_x (float): x-Position der Animation, pos_y (float): y-Position der Animation, rect (pygame.Rect): Rechteck für die Animation, rect_attach (str): Befestigungspunkt des Rechtecks, scale (tuple): Skalierung der Animation, source (str): Pfad zur Bildquelle, solid (bool): Ob die Animation solide ist, is_spritesheet (bool): Ob es sich um ein Sprite-Sheet handelt, fix (bool): Ob die Position fixiert ist, base_sprite (int): Startindex des Sprites, ani_frames_count (int): Anzahl der Animationsframes, ani_animations (dict): Wörterbuch der Animationen.
    """
    def __init__(self, pos_x, pos_y, rect = entities.pygame.Rect(0,0,64,64), rect_attach = "center", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\pick_up.png", solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=4, ani_animations={"pick_up": [0,3,5,False]}):
        """
        Initialisiert die Pick-Up-Animation mit den angegebenen Parametern.
        Parameter: pos_x (float): x-Position der Animation, pos_y (float): y-Position der Animation, rect (pygame.Rect): Rechteck für die Animation, rect_attach (str): Befestigungspunkt des Rechtecks, scale (tuple): Skalierung der Animation, source (str): Pfad zur Bildquelle, solid (bool): Ob die Animation solide ist, is_spritesheet (bool): Ob es sich um ein Sprite-Sheet handelt, fix (bool): Ob die Position fixiert ist, base_sprite (int): Startindex des Sprites, ani_frames_count (int): Anzahl der Animationsframes, ani_animations (dict): Wörterbuch der Animationen.
        """
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

    def update(self, dx=0, dy=0, *args):
        """
        Aktualisiert die Animation.
        Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, *args: Zusätzliche Argumente.
        Rückgabe: Ergebnis der übergeordneten Update-Methode.
        """
        return super().update(dx, dy, *args)
    
class interact_animation(entities.Entity):
    """
    Animation für Interaktionen.
    Parameter: pos_x (float): x-Position der Animation, pos_y (float): y-Position der Animation, rect (pygame.Rect): Rechteck für die Animation, rect_attach (str): Befestigungspunkt des Rechtecks, scale (tuple): Skalierung der Animation, source (str): Pfad zur Bildquelle, solid (bool): Ob die Animation solide ist, is_spritesheet (bool): Ob es sich um ein Sprite-Sheet handelt, fix (bool): Ob die Position fixiert ist, base_sprite (int): Startindex des Sprites, ani_frames_count (int): Anzahl der Animationsframes, ani_animations (dict): Wörterbuch der Animationen.
    """
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64),rect_attach = "center", scale = (64, 64), source = r"Sprites_Main/InteractionAnimation.png", solid = False, is_spritesheet = True, fix=False, base_sprite=0, ani_frames_count=43, ani_animations={"interaction": [0,42, 1, False]}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
    