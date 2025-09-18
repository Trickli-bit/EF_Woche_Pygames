import Engine.entities as entities
import pygame
import Main.settings as settings
import Engine.Entity_Classes.collectable as collectable
import Main.generation as generation
import Main.sounds as sounds
class Wall(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Wall.png", solid = True, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=8, ani_animations={}, flip = (False, False)):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

        if flip is not (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])

class Water(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0, 0, 64, 64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Water.png", solid = True, is_spritesheet = True, fix=False, base_sprite=0, ani_frames_count=8, ani_animations={}, flip = (False, False)):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

        if flip is not (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])
class Laser_h(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Laser_h.png", solid = True, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={"turn_off_laser": [3, 6, 14, False], "standard": [0,1, 3, True]}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.Animation.start_animation("standard")

        self.near_items = []
        self.dying = False
        self.dying_counter = 0

    def die(self, entities):
        if not self.dying:
            self.near_items.clear()
            # Mittelpunkt des Screens
            center_x = settings.SCREEN_WIDTH // 2
            center_y = settings.SCREEN_HEIGHT // 2
            max_distance = 400  # 300 Blöcke in Pixeln

            # Variable für Ergebnis

            for entity in entities:
                if isinstance(entity, collectable.Collectable):
                    if entity.should_pick_up == False:
                        dx = abs(entity.rect.x - center_x)
                        dy = abs(entity.rect.y - center_y)
                        d = ((dy)**2 + (dx)**2)**(0.5)

                        # Prüfen, ob innerhalb von 300 Blöcken in beide Richtungen
                        if d <= max_distance:
                            if (entity.name, entity) not in self.near_items:
                                self.near_items.append((entity.name, entity))

            amount_stick = generation.GetNumberOfItems("Stick") + 1
            amount_rock = generation.GetNumberOfItems("Rock") + 1
            amount_mushroom = generation.GetNumberOfItems("Mushroom_juice") + 1


            price_stick = 0
            price_rock = 0
            price_mushroom = 0


            for name, entity_found in self.near_items:
                if name == "Stick":
                    price_stick += 1
                elif name == "Rock":
                    price_rock += 1
                elif name == "Mushroom_juice":
                    price_mushroom += 1

            if price_stick <= amount_stick and price_rock <= amount_rock and price_mushroom <= amount_mushroom:
                for i in range(price_stick):
                    generation.removeItemFromInventory("Stick")
                for i in range(price_rock):
                    generation.removeItemFromInventory("Rock")
                for i in range(price_mushroom):
                    generation.removeItemFromInventory("Mushroom_juice")
                self.dying = True
            
                for entity in entities:
                # Check if entity is a laser (both horizontal and vertical)
                    if isinstance(entity, (Laser_h, Laser_v)):
                        if entity is not self:  # Don't deactivate the current laser twice
                            dx = entity.rect.centerx - self.rect.centerx
                            dy = entity.rect.centery - self.rect.centery
                            distance = (dx**2 + dy**2) ** 0.5
                            if distance <= 450:
                                entity.dying = True

    def update(self, dx=0, dy=0, *args):
        super().update(dx, dy, *args)
        if self.dying:
            sounds.laser_aus()
            self.dying_counter += 1
            self.Animation.start_animation("turn_off_laser")
            if self.dying_counter == 50:
                self.kill()

class Laser_v(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = pygame.Rect(0,0,64,64), rect_attach = "topleft", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\Laser_v.png", solid = True, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=5, ani_animations={"turn_off_laser": [3, 6, 7, False], "standard": [0, 1, 3, True]}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.Animation.start_animation("standard")

        self.near_items = []
        self.dying = False
        self.dying_counter = 0

    def die(self, entities):
        if not self.dying:
            self.near_items.clear()
            # Mittelpunkt des Screens
            center_x = settings.SCREEN_WIDTH // 2
            center_y = settings.SCREEN_HEIGHT // 2
            max_distance = 400  # 300 Blöcke in Pixeln

            # Variable für Ergebnis

            for entity in entities:
                if isinstance(entity, collectable.Collectable):
                    if entity.should_pick_up == False:
                        dx = abs(entity.rect.x - center_x)
                        dy = abs(entity.rect.y - center_y)
                        d = ((dy)**2 + (dx)**2)**(0.5)
                        # Prüfen, ob innerhalb von 300 Blöcken in beide Richtungen
                        if d <= max_distance:
                            if (entity.name, entity) not in self.near_items:
                                self.near_items.append((entity.name, entity))

            amount_stick = generation.GetNumberOfItems("Stick") + 1
            amount_rock = generation.GetNumberOfItems("Rock") + 1
            amount_mushroom = generation.GetNumberOfItems("Mushroom_juice") + 1


            price_stick = 0
            price_rock = 0
            price_mushroom = 0

            for name, entity_found in self.near_items:
                if name == "Stick":
                    price_stick += 1
                elif name == "Rock":
                    price_rock += 1
                elif name == "Mushroom_juice":
                    price_mushroom += 1

            if price_stick <= amount_stick and price_rock <= amount_rock and price_mushroom <= amount_mushroom:
                for i in range(price_stick):
                    generation.removeItemFromInventory("Stick")
                for i in range(price_rock):
                    generation.removeItemFromInventory("Rock")
                for i in range(price_mushroom):
                    generation.removeItemFromInventory("Mushroom_juice")
                self.dying = True
            
                for entity in entities:
                # Check if entity is a laser (both horizontal and vertical)
                    if isinstance(entity, (Laser_h, Laser_v)):
                        if entity is not self:  # Don't deactivate the current laser twice
                            dx = entity.rect.centerx - self.rect.centerx
                            dy = entity.rect.centery - self.rect.centery
                            distance = (dx**2 + dy**2) ** 0.5
                            if distance <= 450:
                                entity.dying = True


    def update(self, dx=0, dy=0, *args):
        super().update(dx, dy, *args)
        if self.dying:
            sounds.laser_aus()
            self.dying_counter += 1
            self.Animation.start_animation("turn_off_laser")
            if self.dying_counter == 50:
                self.kill()