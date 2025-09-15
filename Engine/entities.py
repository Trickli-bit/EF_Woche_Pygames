import pygame
import Engine.sprite_sheet as sprite_sheet
import Main.settings as settings

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix = False, base_sprite = 0, ani_frames_count = 0, ani_animations = {}):
        super().__init__()

        """Klasse zur Erstellung von Entitäten (Alle Dinge die ein Sprite besitzen und nicht zum Hintergrund gehören)
        param: \t pos_x, pos_y, (pos_x = 0, pos_y = 0, breite, höhe) Rechteck_attachment, Skalierung, Pfad, Ist_SpriteSheet?, Solid?, Basis Sprite, Anz. Frames, Animationen in einem Dict mit {"Animationsname" : [1. Frame, letztes Frame, geschwindigkeit, loop (bolean)]}"""

        self.fix = fix
        self.rect_attach = rect_attach
        self.is_spritesheet = is_spritesheet
        self.last_animation = (None, False) 
        self.solid = solid
        self.pos_x = pos_x
        self.pos_y = pos_y


        if is_spritesheet:
            self.Animation = sprite_sheet.SpriteSheetAnimation(source, rect, ani_frames_count, ani_animations)
            self.image = self.Animation.frames[base_sprite]
        else:
            self.Animation = sprite_sheet.SpriteSheet(source)
            self.image = self.Animation.sprite_extraction(rect)

        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        
        setattr(self.rect, self.rect_attach, (self.pos_x, self.pos_y))
        rect.x = self.pos_x
        rect.y = self.pos_y
        
    def update(self, dx = 0, dy = 0, *args):
        # Animation aktualisieren
        if self.is_spritesheet:
            self.Animation.update()
        if not self.fix:
            self.rect.x += dx
            self.rect.y += dy


 

class EntityMovable(Entity):
    
            
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix = False, base_sprite = 0, ani_frames_count=0, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        
        """Entität die sich bewegen kann. Erbt von Entity.
        param: \t pos_x, pos_y, breite, höhe, Rechteck_attachment, Skalierung, Pfad, Ist_SpriteSheet?, Basis Sprite, Anz. Frames, Animationen in einem Dict mit {"Animationsname" : [start Frame, letztes Frame, geschwindigkeit, loop (bolean)] ---> Standart: "walking", "walking_s", "walking_w" -> Dabei soll immer ein Frame zuvor für das Standartframe sein.]}"""
        # Afubau SpriteSheet Frame 1: standarfframe walking, 2-n walking animation, n+1: standardframe walking_s, n+2 - m walking_s animation, m+1: standardframe walking_w, m+2 - x walking_w animation
        self.dx = 0
        self.dy = 0
        self.speed = 3
        self.flip = False
        self.animation_name = None
        self.solid_collision_direction = ""

    def animation_movement_adjustement(self):
        """
        Passt die Animation je nach Bewegungsrichtung an.
        Erwartet Animationsnamen: 'walking', 'walking_s', 'walking_w'.
        Bei Bewegung nach links wird das Bild geflippt.
        Startet Animation nur, wenn sie sich ändert. Stoppt nur bei Stillstand.
        """
        
        if self.dx > 0:
            self.animation_name = 'walking'
            self.flip = False
        elif self.dx < 0:
            self.animation_name = 'walking'
            self.flip = True
        elif self.dy < 0:
            self.animation_name = 'walking_w'
        elif self.dy > 0:
            self.animation_name = 'walking_s'

        if self.is_spritesheet:

            if self.dx == 0 and self.dy == 0 and self.last_animation != (None, False):
                self.last_animation = (None, self.flip)
                self.Animation.stop_animation(self.Animation.current_range[0] -1)
                self.image = self.Animation.image
                if self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.animation_name = None
            else:
                if self.last_animation != (self.animation_name, self.flip):
                    self.Animation.stop_animation(self.Animation.current_range[0] -1)
                    self.Animation.start_animation(self.animation_name)
                    self.last_animation = (self.animation_name, self.flip)
            self.image = self.Animation.image
            if self.flip:
                self.image = pygame.transform.flip(self.image, True, False)
        

    def collition(self, pos_x=0, pos_y=0):
        """ Bestimmt die Richtung der Kollision mit einem soliden Objekt.
        param:\t pos_x, pos_y (Position des soliden Objekts)"""
        if self.rect.x > pos_x + settings.SOLID_FRAME_HIGHT / 2:
            self.solid_collision_direction = "right"
        if self.rect.x < pos_x - settings.SOLID_FRAME_HIGHT / 2:
            self.solid_collision_direction = "left"
        if self.rect.y > pos_y + settings.SOLID_FRAME_HIGHT / 2:
            self.solid_collision_direction = "down"
        if self.rect.y < pos_y - settings.SOLID_FRAME_HIGHT / 2:
            self.solid_collision_direction = "up"

    def update(self, dx = 0, dy = 0, *args):

        """ Aktualisiert die Position und Animation der beweglichen Entität.
        param:\t keys (pygame.key.get_pressed()) """

        super().update(dx, dy, *args)
        self.animation_movement_adjustement()
