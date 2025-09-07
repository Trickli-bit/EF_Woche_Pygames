import pygame

class SpriteSheet(pygame.sprite.Sprite):

    def __init__(self, filename):
        """Ladet das SpriteSheet.
        para: \t Pfad(str)"""
        super().__init__()
        try: 
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Fehler beim Laden des Spritesheet Bildes: {filename}")
            raise SystemExit(e)

    def sprite_extraction(self, rectangle):
        """Lädt ein spezifischer Ausschnitt aus einem SpriteSheet
        para: \t Rechteck mit Angaben x,y - width, height (Tupel)
        return: image (pygame.image)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0,0), rect)
        return image
    
    def sprites(self,rects):
        """lädt mehrere Sprites in eine Liste. 
        para: \t Liste von Rects (list)
        return: liste aus images (list)"""
        return [self.sprite_extraction(rect) for rect in rects]
    
    def load_sprites(self, rect, image_count):
        """ Lädt eine Anzahl von Sprites -> image_count aus einem Spritesheet anhand der Grösse des einzelnen Sprite -> rect.
        param:\t Rechteck zu bestimmung der Grösse eines Sprite (pygame.rect, Tupel mit (posx, posy, width, height))\n
        \t Anz. der Bilder (int)
        return: \t liste mit Sprites (list)"""
        tups = [(rect[0] + rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.sprites(tups)
    
class SpriteSheetAnimation(SpriteSheet):

    def __init__(self, filename, rect, image_count, animations):
        """ Erstellt die Sprites für eine Animation 
        param:\t Pfad zum Sprite (r"str) !Standard: 1. frame: Standard 
        param:\t Rechteck zur Bestimmung der Grösse eines Sprites (pygame.rect, Tupel mit (posx, posy, width, height))
        param:\t Anzahl der Sprites (int) 
        param:\t Dictionary mit Name der Animation und Liste mit Range der Animation (dict("str": list(start, end, speed, loop(bolean))))"""
        super().__init__(filename)

        self.animations = animations
        self.active = False
        self.framecounter = 0

        self.frames = self.load_sprites(rect, image_count)
        self.standardframe = self.frames[0]
        self.loop = True
        self.image = self.standardframe 

    def start_animation(self, animation_type):
        """ Startet eine bestimmte Animation.
        param:\t Name der Animation (str) 
        param:\t Wiederholung der Animation (bool, Default=True)"""
        if animation_type not in self.animations:
            raise ValueError(f"Animation '{animation_type}' nicht definiert")
        self.active = True
        self.current_range = self.animations[animation_type]
        self.loop = self.current_range[3]
        self.current_frame = self.current_range[0]

    def next_frame(self):
        """ Berechnet den nächsten Frame der aktuellen Animation.
        return:\t Index des aktuellen Frames (int)"""
        if self.framecounter >= self.current_range[2]:
            self.framecounter = 0
            self.current_frame += 1
            if self.current_frame >= self.current_range[1] + 1:
                if not self.loop:
                    self.stop_animation()
                self.current_frame = self.current_range[0]
                print("reset")
        self.framecounter += 1
        return self.current_frame
    
    def stop_animation(self):
        """ Stoppt die aktuelle Animation und setzt das Bild zurück auf den ersten Frame."""
        self.image = self.frames[0]
        self.active = False
    
    def update_image(self):
        """ Aktualisiert das Bild (self.image) mit dem nächsten Frame der Animation."""
        self.image = self.frames[self.next_frame()]

    def update(self):
        """ Wird von pygame.sprite.Group() automatisch aufgerufen, um das Sprite zu aktualisieren.
        Führt update_image() aus."""
        if self.active == True:
            self.update_image()
