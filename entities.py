import pygame
import sprite_sheet

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, is_spritesheet, base_sprite = 0, ani_frames_count = 0, ani_animations = {}):
        super().__init__()

        """Klasse zur Erstellung von Entitäten (Alle Dinge die ein Sprite besitzen und nicht zum Hintergrund gehören)
        param: \t pos_x, pos_y, breite, höhe, Rechteck_attachment, Skalierung, Pfad, Ist_SpriteSheet?, Basis Sprite, Anz. Frames, Animationen in einem Dict mit {"Animationsname" : [1. Frame, letztes Frame, geschwindigkeit, loop (bolean)]}"""

        self.rect_attach = rect_attach
        self.is_spritesheet = is_spritesheet

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
            self.image = self.Animation.image
        


 

class EntityMovable(Entity):
    
            
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, is_spritesheet, base_sprite = 0, ani_frames_count=0, ani_animations={}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, is_spritesheet, base_sprite, ani_frames_count, ani_animations)
        self.dx = 0
        self.dy = 0
        self.speed = 3

    def animation_movement_adjustement(self, dx, dy):
        """
        Passt die Animation je nach Bewegungsrichtung an.
        Erwartet Animationsnamen: 'walking', 'walking_s', 'walking_w'.
        Bei Bewegung nach links wird das Bild geflippt.
        Startet Animation nur, wenn sie sich ändert. Stoppt nur bei Stillstand.
        """
        animation_name = None
        flip = False
        if self.dx > 0:
            animation_name = 'walking'
            flip = False
        elif self.dx < 0:
            animation_name = 'walking'
            flip = True
        elif self.dy < 0:
            animation_name = 'walking_w'
        elif self.dy > 0:
            animation_name = 'walking_s'

        if self.is_spritesheet:
            if not hasattr(self, '_last_animation'):
                self._last_animation = None
            if self.dx == 0 and self.dy == 0:
                if self._last_animation is not None:
                    self.Animation.stop_animation()
                    self._last_animation = None
            elif animation_name:
                if self._last_animation != (animation_name, flip):
                    self.Animation.start_animation(animation_name)
                    self._last_animation = (animation_name, flip)
                # Bild setzen und ggf. flippen
                image = self.Animation.image
                if flip:
                    image = pygame.transform.flip(image, True, False)
                self.image = image

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

        # Diagonalbewegung anpassen (optional, für gleichmäßige Geschwindigkeit)
        if self.dx != 0 and self.dy != 0:
            self.dx = int(self.dx / 1.4142)
            self.dy = int(self.dy / 1.4142)

        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self, keys):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.calculating_movement(keys)
        self.animation_movement_adjustement(self.dx, self.dy)
