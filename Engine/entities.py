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
        # Animation nur aktualisieren UND auf self.image übernehmen, wenn:
        # - die Entität tatsächlich Animationen definiert hat (ani_animations != {})
        #   -> normale animierbare Entitäten (z.B. NPCs, pick_up, Player)
        # - ODER wenn eine Animation extern gestartet wurde und aktiv ist (sicherheit)
        if self.is_spritesheet:
            should_update_image = False
            if self.ani_animations and len(self.ani_animations) > 0:
                should_update_image = True
            elif getattr(self.Animation, "active", False):
                should_update_image = True

            if should_update_image:
                # Advance animation frames
                self.Animation.update()
                # Aktualisiere self.image nur für animierte Entities (so behalten statische Tiles ihr initial gesetztes Bild)
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
        """
        Passt die Animation je nach Bewegungsrichtung an.
        - Wählt zuerst die gewünschte Richtung (desired).
        - Wenn genau passende Animation (z.B. 'walking_a') existiert, nutze sie, kein Flip.
        - Falls nur die Gegenrichtung existiert (z.B. nur 'walking_d' vorhanden),
          nutze diese und flippe horizontal (nur für links/rechts).
        - Wenn keine passende Animation existiert, ändere nichts.
        """

        # Bestimme Wunschrichtung
        desired = None
        if self.dx > 0:
            desired = 'walking_d'
        elif self.dx < 0:
            desired = 'walking_a'
        elif self.dy < 0:
            desired = 'walking_w'
        elif self.dy > 0:
            desired = 'walking_s'

        # Wähle Animation und ob wir flippen müssen
        anim_to_start = None
        flip_needed = False

        if desired is not None:
            # benutze direkte Animation, falls vorhanden
            if desired in getattr(self, "ani_animations", {}):
                anim_to_start = desired
                flip_needed = False
            else:
                # fallback: versuche die Gegenrichtung (opposite)
                opposite_map = {
                    'walking_a': 'walking_d',
                    'walking_d': 'walking_a',
                    'walking_w': 'walking_s',
                    'walking_s': 'walking_w'
                }
                opp = opposite_map.get(desired)
                if opp and opp in getattr(self, "ani_animations", {}):
                    anim_to_start = opp
                    # Flip nur horizontal, nicht vertikal
                    flip_needed = True if desired in ('walking_a', 'walking_d') else False

        # setze flip-flag (wichtig falls vorher ein anderer Wert da war)
        self.flip = flip_needed

        # Wenn Spritesheet vorhanden: starte/stoppe Animationen korrekt und aktualisiere self.image
        if self.is_spritesheet:
            # Stillstand -> Zurück auf Standframe
            if self.dx == 0 and self.dy == 0 and self.last_animation != (None, False):
                self.last_animation = (None, self.flip)
                # stoppe aktuelle Animation
                try:
                    self.Animation.stop_animation(self.Animation.current_range[1] + 1)
                except Exception:
                    pass
                # setze das Image auf das, was Animation momentan liefert (skalieren & flip falls nötig)
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
                # Wenn eine Animation gewählt wurde: starte sie falls sie neu ist
                if anim_to_start is not None:
                    if self.last_animation != (anim_to_start, self.flip):
                        try:
                            self.Animation.stop_animation(self.Animation.current_range[1] + 1)
                        except Exception:
                            pass
                        self.Animation.start_animation(anim_to_start)
                        self.last_animation = (anim_to_start, self.flip)
                # sync aktuelles Frame ins sichtbare Bild (auch wenn gleiche Animation läuft)
                try:
                    img = self.Animation.image
                    img = pygame.transform.scale(img, self.scale)
                    if self.flip:
                        img = pygame.transform.flip(img, True, False)
                    self.image = img
                except Exception:
                    pass


    def collition(self, entity):
        """Berechnet die Kollisionsrichtung"""

        # Richtung bestimmen und Entität anhalten
        if self.dx == 0 and self.dy < 0:
            self.dy = 0
            self.solid_collision_direction = "up"
        # nach oben
        elif self.dx == 0 and self.dy > 0:
            self.dy = 0
            self.solid_collision_direction = "down"
        # nach unten
        elif self.dx > 0 and self.dy == 0:
            self.dx = 0
            self.solid_collision_direction = "right"
        # nach links
        elif self.dx < 0 and self.dy == 0:
            self.dx = 0
            self.solid_collision_direction = "left"
        # nach rechts
        elif self.dx > 0 and self.dy > 0:
            self.dx = 0
            self.dy = 0
            self.solid_collision_direction = "leftup"
        # nach links unten
        elif self.dx < 0 and self.dy > 0:
            self.dx = 0
            self.dy = 0
            self.solid_collision_direction = "leftdown"
        # nach links oben
        elif self.dx > 0 and self.dy < 0:
            self.dx = 0
            self.dy = 0
            self.solid_collision_direction = "rightup"
        # nach rechts unten
        elif self.dx < 0 and self.dy < 0:
            self.dx = 0
            self.dy = 0
            self.solid_collision_direction = "rightdown"
        # nach rechts oben


    def update(self, dx = 0, dy = 0, *args):
        super().update(dx, dy, *args)
        self.animation_movement_adjustement()