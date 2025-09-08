import pygame
import sprite_sheet

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, is_spritesheet, base_sprite = 0, ani_frames_count = 0, ani_animations = {}):
        super().__init__()

        """Klasse zur Erstellung von Entitäten (Alle Dinge die ein Sprite besitzen und nicht zum Hintergrund gehören)
        param: \t pos_x, pos_y, breite, höhe, Rechteck_attachment, Skalierung, Pfad, Ist_SpriteSheet?, Basis Sprite, Anz. Frames, Animationen in einem Dict mit {"Animationsname" : [1. Frame, letztes Frame, geschwindigkeit, loop (bolean)]}"""

        self.rect_attach = rect_attach
        self.is_spritesheet = is_spritesheet
        self.last_animation = (None, False) 

        if is_spritesheet:
            self.Animation = sprite_sheet.SpriteSheetAnimation(source, rect, ani_frames_count, ani_animations)
            self.image = self.Animation.frames[base_sprite]
        else:
            self.Animation = sprite_sheet.SpriteSheet(source)
            self.image = self.Animation.sprite_extraction(rect)

        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        
        setattr(self.rect, self.rect_attach, (pos_x, pos_y))
        
    def update(self, *args):
        # Animation aktualisieren
        if self.is_spritesheet:
            self.Animation.update()
        


 

class EntityMovable(Entity):
    
            
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, is_spritesheet, base_sprite = 0, ani_frames_count=0, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
        
        """Entität die sich bewegen kann. Erbt von Entity.
        param: \t pos_x, pos_y, breite, höhe, Rechteck_attachment, Skalierung, Pfad, Ist_SpriteSheet?, Basis Sprite, Anz. Frames, Animationen in einem Dict mit {"Animationsname" : [start Frame, letztes Frame, geschwindigkeit, loop (bolean)] ---> Standart: "walking", "walking_s", "walking_w" -> Dabei soll immer ein Frame zuvor für das Standartframe sein.]}"""
        # Afubau SpriteSheet Frame 1: standarfframe walking, 2-n walking animation, n+1: standardframe walking_s, n+2 - m walking_s animation, m+1: standardframe walking_w, m+2 - x walking_w animation
        self.dx = 0
        self.dy = 0
        self.speed = 3
        self.flip = False
        self.animation_name = None

    def animation_movement_adjustement(self, dx, dy):
        """
        Passt die Animation je nach Bewegungsrichtung an.
        Erwartet Animationsnamen: 'walking', 'walking_s', 'walking_w'.
        Bei Bewegung nach links wird das Bild geflippt.
        Startet Animation nur, wenn sie sich ändert. Stoppt nur bei Stillstand.
        param:\t dx, dy (int)
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
        
                    
    def calculating_movement(self, keys):

        """ Berechnet die Bewegung basierend auf den gedrückten Tasten.
        param:\t keys (pygame.key.get_pressed()) """

        self.dx = self.dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx += self.speed

        # Diagonalbewegung anpassen (optional, für gleichmäßige Geschwindigkeit)
        if self.dx != 0 and self.dy != 0:
            self.dx = int(self.dx / 1.4142)
            self.dy = int(self.dy / 1.4142)

        self.rect.x += self.dx
        self.rect.y += self.dy

    def collition(self):
        

    def update(self, keys):

        """ Aktualisiert die Position und Animation der beweglichen Entität.
        param:\t keys (pygame.key.get_pressed()) """

        super().update()
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.calculating_movement(keys)
        self.animation_movement_adjustement(self.dx, self.dy)
