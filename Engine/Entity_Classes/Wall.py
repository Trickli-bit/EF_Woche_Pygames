import Engine.entities as entities
import pygame
import Main.settings as settings
import Engine.Entity_Classes.collectable as collectable

class Wall(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Wall.png", solid = True, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=8, ani_animations={}, flip = (False, False)):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

        if flip is not (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])

class Laser_h(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Laser_h.png", solid = True, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={"turn_off_laser": [3, 6, 7, False], "standard": [0,1, 3, True]}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.Animation.start_animation("standard")

        self.near_items = []

    def die(self, entities):
        # Mittelpunkt des Screens
        center_x = settings.SCREEN_WIDTH // 2
        center_y = settings.SCREEN_HEIGHT // 2
        max_distance = 1000  # 300 Blöcke in Pixeln

        # Variable für Ergebnis

        for entity in entities:
            if isinstance(entity, collectable.Collectable):
                if entity.should_pick_up == False:
                    dx = abs(entity.rect.x - center_x)
                    dy = abs(entity.rect.y - center_y)
                    d = ((dy)**2 + (dx)**2)**(0.5)
                    print("Distances", entity.pos_x, entity.pos_y, dy, dx, d, max_distance)

                    # Prüfen, ob innerhalb von 300 Blöcken in beide Richtungen
                    if d <= max_distance:
                        print("there is one close")
                        if (entity.name, entity) not in self.near_items:
                            self.near_items.append((entity.name, entity))
                        break  # optional, wenn nur wissen willst, ob mindestens eins in der Nähe ist

        print(self.near_items)


class Laser_v(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Laser_v.png", solid = True, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={"turn_off_laser": [3, 6, 7, False], "standard": [0, 1, 3, True]}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.Animation.start_animation("standard")

        self.near_items = []

    def die(self, entities):
        # Mittelpunkt des Screens
        center_x = settings.SCREEN_WIDTH // 2
        center_y = settings.SCREEN_HEIGHT // 2
        max_distance = 64*5  # 300 Blöcke in Pixeln

        # Variable für Ergebnis

        for entity in entities:
            if isinstance(entity, collectable.Collectable):
                if entity.should_pick_up == False:
                    print("Theater are such items")
                    dx = abs(entity.pos_x - center_x)
                    dy = abs(entity.pos_y - center_y)
                    d = ((dy)**2 + (dx)**2)**(0.5)

                    # Prüfen, ob innerhalb von 300 Blöcken in beide Richtungen
                    if d <= max_distance:
                        print("there is one close")
                        if (entity.name, entity) not in self.near_items:
                            self.near_items.append((entity.name, entity))
                        break  # optional, wenn nur wissen willst, ob mindestens eins in der Nähe ist

        print(self.near_items)