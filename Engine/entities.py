# Engine/entities.py  (ersetzt die Entity- und EntityMovable-Klassen)

import pygame
import Engine.sprite_sheet as sprite_sheet
import Main.settings as settings

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix = False, base_sprite = 0, ani_frames_count = 0, ani_animations = {}):
        super().__init__()

        """Klasse zur Erstellung von Entitäten (Alle Dinge die ein Sprite besitzen und nicht zum Hintergrund gehören)
        param: \t pos_x (int), pos_y, (int) (pos_x = 0, pos_y = 0, breite, höhe) Rechteck_attachment (str), Skalierung (int), Pfad (r-str), Ist_SpriteSheet? (boolean), Solid? (boolean), Basis Sprite (int), Anz. Frames (int), Animationen in einem Dict mit {"Animationsname" : [1. Frame, letztes Frame, geschwindigkeit, loop (bolean)]}"""

        self.fix = fix
        self.rect_attach = rect_attach
        self.scale = scale
        self.is_spritesheet = is_spritesheet
        self.last_animation = (None, False)
        self.solid = solid
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ani_animations = ani_animations

        # wichtig für späteres Rescaling / base-frame
        self.scale = scale
        self.base_sprite = base_sprite
        self.ani_frames_count = ani_frames_count

        if is_spritesheet:
            # Animation-Objekt pro-Instanz (frames werden intern gecached)
            self.Animation = sprite_sheet.SpriteSheetAnimation(source, rect, ani_frames_count, ani_animations, base_sprite)

            # Setze das sichtbare Bild initial auf das base_sprite (so bleiben Tiles korrekt)
            try:
                base_img = self.Animation.frames[self.base_sprite]
            except Exception:
                # Fallback: das standardframe der Animation
                base_img = getattr(self.Animation, "standardframe", self.Animation.frames[0])
            self.image = pygame.transform.scale(base_img, self.scale)
        else:
            self.Animation = sprite_sheet.SpriteSheet(source)
            self.image = self.Animation.sprite_extraction(rect)
            self.image = pygame.transform.scale(self.image, self.scale)


        self.rect = self.image.get_rect()
        setattr(self.rect, self.rect_attach, (self.pos_x, self.pos_y))
        if self.rect_attach == "topleft":
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
        else:
            rect.x = self.pos_x
            rect.y = self.pos_y
        
    def update(self, dx = 0, dy = 0, *args):
        """Aktualisiert die Entität.    
        Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, *args: Zusätzliche Argumente.
        Rückgabe: Ergebnis der übergeordneten Update-Methode.
        """
        super().update(dx, dy, *args)
        if self.is_spritesheet:
            should_update_image = False
            if self.ani_animations and len(self.ani_animations) > 0:
                should_update_image = True
            elif getattr(self.Animation, "active", False):
                should_update_image = True

            if should_update_image:
                self.Animation.update()
                try:
                    new_img = self.Animation.image
                    new_img = pygame.transform.scale(new_img, self.scale)
                    # Falls die Entität ein flip-Flag hat (movable entities), flip hier
                    if getattr(self, "flip", False):
                        new_img = pygame.transform.flip(new_img, True, False)
                    self.image = new_img
                except Exception:
                    # keep current image on error
                    pass

        if not self.fix:
            self.rect.x += dx
            self.rect.y += dy

class EntityMovable(Entity):
    """
    Entität die sich bewegen kann. Erbt von Entity.
    Parameter: pos_x (float): x-Position der Animation, pos_y (float): y-Position der Animation, rect (pygame.Rect): Rechteck für die Animation, rect_attach (str): Befestigungspunkt des Rechtecks, scale (tuple): Skalierung der Animation, source (str): Pfad zur Bildquelle, solid (bool): Ob die Animation solide ist, is_spritesheet (bool): Ob es sich um ein Sprite-Sheet handelt, fix (bool): Ob die Position fixiert ist, base_sprite (int): Startindex des Sprites, ani_frames_count (int): Anzahl der Animationsframes, ani_animations (dict): Wörterbuch der Animationen.
    """

    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix = False, base_sprite = 0, ani_frames_count=0, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        
        """Entität die sich bewegen kann. Erbt von Entity."""
        self.dx = 0
        self.dy = 0
        self.speed = 3
        self.flip = False
        self.animation_name = None
        self.solid_collision_direction = None

    def animation_movement_adjustement(self):
        """ Passt die Animation basierend auf der Bewegungsrichtung an.
        Wenn sich die Entität bewegt, wird die entsprechende Animation gestartet.
        Wenn die Entität stillsteht, wird die Animation gestoppt und das Bild auf den Standframe gesetzt.
        """

        desired = None
        if self.dx > 0:
            desired = 'walking_d'
        elif self.dx < 0:
            desired = 'walking_a'
        elif self.dy < 0:
            desired = 'walking_w'
        elif self.dy > 0:
            desired = 'walking_s'

        anim_to_start = None
        flip_needed = False

        if desired is not None:
            if desired in getattr(self, "ani_animations", {}):
                anim_to_start = desired
                flip_needed = False
            else:
                opposite_map = {
                    'walking_a': 'walking_d',
                    'walking_d': 'walking_a',
                    'walking_w': 'walking_s',
                    'walking_s': 'walking_w'
                }
                opp = opposite_map.get(desired)
                if opp and opp in getattr(self, "ani_animations", {}):
                    anim_to_start = opp
                    flip_needed = True if desired in ('walking_a', 'walking_d') else False

        self.flip = flip_needed

        if self.is_spritesheet:
            
            if self.dx == 0 and self.dy == 0 and self.last_animation != (None, False):
                self.last_animation = (None, self.flip)
                
                try:
                    self.Animation.stop_animation(self.Animation.current_range[1] + 1)
                except Exception:
                    pass
                
                try:
                    img = self.Animation.image
                    img = pygame.transform.scale(img, self.scale)
                    if self.flip:
                        img = pygame.transform.flip(img, True, False)
                    self.image = img
                except Exception:
                    pass
                self.animation_name = None
            else:
                
                if anim_to_start is not None:
                    if self.last_animation != (anim_to_start, self.flip):
                        try:
                            self.Animation.stop_animation(self.Animation.current_range[1] + 1)
                        except Exception:
                            pass
                        self.Animation.start_animation(anim_to_start)
                        self.last_animation = (anim_to_start, self.flip)
                
                try:
                    img = self.Animation.image
                    img = pygame.transform.scale(img, self.scale)
                    if self.flip:
                        img = pygame.transform.flip(img, True, False)
                    self.image = img
                except Exception:
                    pass


    
        


    def update(self, dx = 0, dy = 0, *args):
        """
        Aktualisiert die bewegliche Entität. 
        Parameter: dx (float): Änderung der x-Position, dy (float): Änderung der y-Position, *args: Zusätzliche Argumente.
        """
        super().update(dx, dy, *args)
        self.animation_movement_adjustement()