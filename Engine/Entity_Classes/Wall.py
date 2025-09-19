import Engine.entities as entities
import pygame
import Main.settings as settings
import Engine.Entity_Classes.collectable as collectable
import Main.generation as generation
import Main.sounds as sounds
import Main.inventoryManager as inventory

class Wall(entities.Entity):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft", scale=(64, 64),
                 source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Wall.png", solid=True,
                 is_spritesheet=True, fix=False, base_sprite=0, ani_frames_count=8, ani_animations={}, flip=(False, False)):
        """Statische Wand, optional gespiegelt."""
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        if flip != (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])
        
        if base_sprite != 0:
            self.solid = False
        


class Water(entities.Entity):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0, 0, 64, 64), rect_attach="topleft", scale=(64, 64),
                 source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Water.png", solid=True,
                 is_spritesheet=True, fix=False, base_sprite=0, ani_frames_count=8, ani_animations={}, flip=(False, False)):
        """Wasserfläche, optional gespiegelt."""
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        if flip != (False, False):
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])


class Laser_h(entities.Entity):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft", scale=(64, 64),
                 source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Laser_h.png", solid=True,
                 is_spritesheet=True, fix=False, base_sprite=0, ani_frames_count=5,
                 ani_animations={"turn_off_laser": [3, 6, 14, False], "standard": [0,1,3,True]}):
        """Horizontaler Laser mit Abschalt-Animation."""
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.Animation.start_animation("standard")
        self.near_items = []
        self.dying = False
        self.dying_counter = 0

    def die(self, entities):
        """Prüft Items und deaktiviert Laser in der Nähe."""
        if not self.dying:
            self.near_items.clear()
            center_x = settings.SCREEN_WIDTH // 2
            center_y = settings.SCREEN_HEIGHT // 2
            max_distance = 400

            for entity in entities:
                if isinstance(entity, collectable.Collectable) and not entity.should_pick_up:
                    dx = abs(entity.rect.x - center_x)
                    dy = abs(entity.rect.y - center_y)
                    d = (dx**2 + dy**2) ** 0.5
                    if d <= max_distance and (entity.name, entity) not in self.near_items:
                        self.near_items.append((entity.name, entity))

            amount_stick = inventory.GetNumberOfItems("Stick") + 1
            amount_rock = inventory.GetNumberOfItems("Rock") + 1
            amount_mushroom = inventory.GetNumberOfItems("Mushroom_juice") + 1
            amount_shell = inventory.GetNumberOfItems("Shell") + 1
            amount_mirror = inventory.GetNumberOfItems("Mirror") + 1

            price_stick = price_rock = price_mushroom = price_mirror = price_shell = 0

            for name, entity_found in self.near_items:
                if name == "Stick": price_stick += 1
                elif name == "Rock": price_rock += 1
                elif name == "Mushroom_juice": price_mushroom += 1
                elif name == "Mirror": price_mirror += 1
                elif name == "Shell": price_shell += 1 

            print("Prices:", price_rock, price_stick, amount_rock, amount_stick)

            if (price_stick <= amount_stick and price_rock <= amount_rock and
                price_mushroom <= amount_mushroom and price_mirror <= amount_mirror and price_shell <= amount_shell):
                for _ in range(price_stick): inventory.removeItemFromInventory("Stick")
                for _ in range(price_rock): inventory.removeItemFromInventory("Rock")
                for _ in range(price_mushroom): inventory.removeItemFromInventory("Mushroom_juice")
                for _ in range(price_mirror): inventory.removeItemFromInventory("Mirror")
                for _ in range(price_shell): inventory.removeItemFromInventory("Shell")
                self.dying = True

                for entity in entities:
                    if isinstance(entity, (Laser_h, Laser_v)) and entity is not self:
                        dx = entity.rect.centerx - self.rect.centerx
                        dy = entity.rect.centery - self.rect.centery
                        if (dx**2 + dy**2) ** 0.5 <= 450:
                            entity.dying = True

    def update(self, dx=0, dy=0, *args):
        """Spielt Abschalt-Animation und entfernt Laser."""
        super().update(dx, dy, *args)
        if self.dying:
            sounds.laser_aus()
            self.dying_counter += 1
            self.Animation.start_animation("turn_off_laser")
            if self.dying_counter == 50:
                self.kill()


class Laser_v(entities.Entity):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft", scale=(64, 64),
                 source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Laser_v.png", solid=True,
                 is_spritesheet=True, fix=False, base_sprite=0, ani_frames_count=5,
                 ani_animations={"turn_off_laser": [3, 6, 7, False], "standard": [0,1,3,True]}):
        """Vertikaler Laser mit Abschalt-Animation."""
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.Animation.start_animation("standard")
        self.near_items = []
        self.dying = False
        self.dying_counter = 0

    def die(self, entities):
        """Prüft Items und deaktiviert Laser in der Nähe."""
        if not self.dying:
            self.near_items.clear()
            center_x = settings.SCREEN_WIDTH // 2
            center_y = settings.SCREEN_HEIGHT // 2
            max_distance = 400

            for entity in entities:
                if isinstance(entity, collectable.Collectable) and not entity.should_pick_up:
                    dx = abs(entity.rect.x - center_x)
                    dy = abs(entity.rect.y - center_y)
                    d = (dx**2 + dy**2) ** 0.5
                    if d <= max_distance and (entity.name, entity) not in self.near_items:
                        self.near_items.append((entity.name, entity))

            amount_stick = inventory.GetNumberOfItems("Stick") + 1
            amount_rock = inventory.GetNumberOfItems("Rock") + 1
            amount_mushroom = inventory.GetNumberOfItems("Mushroom_juice") + 1
            amount_mirror = inventory.GetNumberOfItems("Mirror") + 1
            amount_shell = inventory.GetNumberOfItems("Shell") + 1

            price_stick = price_rock = price_mushroom = price_mirror = price_shell =  0

            for name, entity_found in self.near_items:
                if name == "Stick": price_stick += 1
                elif name == "Rock": price_rock += 1
                elif name == "Mushroom_juice": price_mushroom += 1
                elif name == "Mirror": price_mirror += 1
                elif name == "Shell": price_shell += 1

            print("Prices:", price_rock, price_stick, price_mirror, price_shell, price_mushroom)
            print("Able", amount_rock, amount_stick, amount_mirror, amount_shell, amount_mushroom)

            if (price_stick <= amount_stick and price_rock <= amount_rock and
                price_mushroom <= amount_mushroom and price_mirror <= amount_mirror and price_shell <= amount_shell):
                print("price able to pay")
                for _ in range(price_stick): inventory.removeItemFromInventory("Stick")
                for _ in range(price_rock): inventory.removeItemFromInventory("Rock")
                for _ in range(price_mushroom): inventory.removeItemFromInventory("Mushroom_juice")
                for _ in range(price_mirror): inventory.removeItemFromInventory("Mirror")
                for _ in range(price_shell): inventory.removeItemFromInventory("Shell")
                self.dying = True


                for entity in entities:
                    if isinstance(entity, (Laser_h, Laser_v)) and entity is not self:
                        dx = entity.rect.centerx - self.rect.centerx
                        dy = entity.rect.centery - self.rect.centery
                        if (dx**2 + dy**2) ** 0.5 <= 450:
                            entity.dying = True

    def update(self, dx=0, dy=0, *args):
        """Spielt Abschalt-Animation und entfernt Laser."""
        super().update(dx, dy, *args)
        if self.dying:
            sounds.laser_aus()
            self.dying_counter += 1
            self.Animation.start_animation("turn_off_laser")
            if self.dying_counter == 50:
                self.kill()
