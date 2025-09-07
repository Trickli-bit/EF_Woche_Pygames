import pygame
import sprite_sheet
from main import keys

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, width, height, rect_attach, scale, source, is_spritesheet, base_sprite = 1, ani_frames_count = 0, ani_animations = {}):
        super().__init__()

        """Klasse zur Erstellung von Entitäten (Alle Dinge die ein Sprite besitzen und nicht zum Hintergrund gehören)
        param: \t pos_x, pos_y, breite, höhe, Rechteck_attachment, Skalierung, Pfad, Ist_SpriteSheet?, Basis Sprite, Anz. Frames, Animationen in einem Dict mit {"Animationsname" : [1. Frame, letztes Frame, geschwindigkeit, loop (bolean)]}"""

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.hight = height
        self.base_sprite = base_sprite
        self.is_spritesheet = is_spritesheet
        self.rect_attach = rect_attach
        self.a = True

        if is_spritesheet:
            self.Animation = sprite_sheet.SpriteSheetAnimation(source, pygame.Rect(0, 0, width, height), ani_frames_count, ani_animations)
            self.image = self.Animation.frames[base_sprite]
        else:
            self.Animation = sprite_sheet.SpriteSheet(source)
            self.image = self.Animation.sprite_extraction(pygame.Rect(0, 0, width, height))
        
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect_attach = rect_attach
        self.scale = scale
        setattr(self.rect, self.rect_attach, (pos_x, pos_y))

    def collidable(self):
        pass

    def update(self):
        self.Animation.update()
        self.image = self.Animation.image

        if keys[pygame.K_LEFT] and self.a == True:
            self.a = False
            self.image = pygame.transform.rotate(self.image, 45)
 

class EntityMovable(Entity):
    def __init__(self, pos_x, pos_y, width, height, rect_attach, scale, source, is_spritesheet, base_sprite=1, ani_frames_count=0, ani_animations={}):
        super().__init__(pos_x, pos_y, width, height, rect_attach, scale, source, is_spritesheet, base_sprite, ani_frames_count, ani_animations)

        self.dx = 0
        self.dy = 0
        self.is_moving = False
        self.first_flip = False
        self.current_rotation = 0
        

    def moving(self, dx, dy, animation_type):
        "Verändert die Animation in die richtige Richtung, und die Position der Entity"
        self.is_moving = True
        if not self.is_moving:
            if not self.first_flip and dx > 0:
                pass
            else:
                if dx != 0:
                    self.current_rotation += 180
                
                pass
            self.first_flip = True
            
        self.pos_x += self.dx
        self.pos_y += self.dy   
        
        

        setattr(self.rect, self.rect_attach, (self.pos_x, self.pos_y))
        
    

    def update(self):
        "Abfrage zur Bewegung der Entity"