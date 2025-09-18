import csv
import Engine.Entity_Classes.floor as Floor
import Engine.Entity_Classes.Wall as Wall
import pygame
import Engine.Entity_Classes.inventorySlot as inventory
import Main.settings as settings
import random
import Engine.Entity_Classes.collectable as collectable
import Engine.Entity_Classes.interactable as interactable
import Engine.Entity_Classes.npc as npc
import re


def parse_y_string(s: str):
    """Parst einen String im Format 'Y.<int>.<int>' und gibt die beiden Ganzzahlen zurück."""
    pattern = r"^Y\.(\d+)\.(\d+)$"
    match = re.match(pattern, s)
    if match:
        first_int = int(match.group(1))
        second_int = int(match.group(2))
        return True, first_int, second_int
    return False, None, None


class generateLandscape():

    """
    Generiert die Landschaft basierend auf den CSV-Dateien.
     Liest die CSV-Dateien ein, aktualisiert die Kacheln und generiert Gras-, Wand- und Interaktionsobjekte.
    """
    def __init__(self, spritegroup, entitygroup):
        """
        Initialisiert die Generierungsklasse mit den CSV-Daten und den Sprite-Gruppen. 
        \n param:\t spritegroup (pygame.sprite.Group) - Gruppe für Boden-Sprites. \n param:\t entitygroup (pygame.sprite.Group) 
        - Gruppe für Wand- und Interaktions-Sprites.
        """
    """Liest eine CSV-Datei ein und erstellt eine 2D-Liste der Werte."""
    def __init__(self, spritegroup, entitygroup, trigger):
        """ Initialisiert die Klasse mit dem Dateinamen der CSV-Datei.
        param:\t filename (str) - Pfad zur CSV-Datei."""
        

        self.map = self.readCSV("Main/mapCSV.csv")
        self.map_wall = self.readCSV("Main/mapCSVWall.csv")
        self.map_laser = self.readCSV("Main/mapCSVInteractables.csv")
        self.spritegroup = spritegroup
        self.entitygroup = entitygroup


        """Mapping der CSV-Werte zu Terrain-Typen."""

        self.trigger = trigger
        

        self.elem = {
            0: "grass",
            1: "grass_l_potsoile",
            2: "grass_r_potsoile",
            3: "grass_t_potsoile",
            4: "grass_b_potsoile",
            5: "grass_tl_potsoile",
            6: "grass_tr_potsoile",
            7: "grass_bl_potsoile",
            8: "grass_br_potsoile",
            9: "potsoile",
            10: "wall"
        }

        self.map = self.update_tiles(self.map)
        self.map_wall = self.update_tiles(self.map_wall)

    def readCSV(self, filename):
        """
        Diese Funktion liest eine CSV-Datei ein und gibt die Daten als Liste von Listen zurück.
        :param filename: Der Pfad zur CSV-Datei.
        :return: Eine Liste von Listen, die die Daten der CSV-Datei repräsentieren.
        """

        with open(filename, "r") as file:
            reader = csv.reader(file)
            data = [list(map(int, row)) for row in reader]

        return data
    
    def update_tiles(self, map_):
        """
        Diese Funktion aktualisiert die Kacheln in der Karte basierend auf den Nachbarn.
        """
        height = len(map_) - 2
        width = max((len(r) for r in map_), default=0)

        full = [row[:] + [0] * (width - len(row)) for row in map_]
        new_map = [row[:] for row in full]

        neigh8 = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        def same_terrain(val, prefix):
            if prefix == "F":  # Floor
                return val == 2 or (isinstance(val, str) and val.startswith("F"))
            elif prefix == "R":  # Water
                return val == 1 or (isinstance(val, str) and val.startswith("R"))
            elif prefix == "W":  # Wall
                return val == 3 or (isinstance(val, str) and val.startswith("W"))
            return False

        # Phase 1: F/W/R auf 0er Felder propagieren
        for y in range(height):
            for x in range(width):
                v = full[y][x]
                if v in (1, 2, 3):
                    p = "F" if v == 2 else ("W" if v == 3 else "R")
                    for dy, dx in neigh8:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width and full[ny][nx] == 0:
                            new_map[ny][nx] = p

        def get_tile_code(prefix, top, right, bottom, left, m, y, x):
            """
            Bestimmt den Kachelcode basierend auf den Nachbarn.
            Parameter: prefix (str): "F", "W" oder "R"
            """
            def diag(dy, dx):
                """
                Überprüft, ob die diagonale Nachbarkachel zum gleichen Terrain gehört.
                Parameter: dy (int): -1 oder 1 für die vertikale Richtung.
                """
                ny, nx = y + dy, x + dx
                return 0 <= ny < len(m) and 0 <= nx < len(m[0]) and same_terrain(m[ny][nx], prefix)

            top_left = diag(-1, -1)
            top_right = diag(-1, 1)
            bottom_left = diag(1, -1)
            bottom_right = diag(1, 1)

            # Normale äußere Ecken
            if not top and not right: return prefix + "tr"
            if not top and not left: return prefix + "tl"
            if not bottom and not right: return prefix + "br"
            if not bottom and not left: return prefix + "bl"

            # Innere Ecken nur für W und R
            if prefix in ("W", "R"):
                if top and left and not top_left: return prefix + "ic_tl"
                if top and right and not top_right: return prefix + "ic_tr"
                if bottom and left and not bottom_left: return prefix + "ic_bl"
                if bottom and right and not bottom_right: return prefix + "ic_br"

            # Kanten
            if not top: return prefix + "t"
            if not right: return prefix + "r"
            if not bottom: return prefix + "b"
            if not left: return prefix + "l"

            # Innenbereich
            return 2 if prefix == "F" else (3 if prefix == "W" else 1)

        def compute_once(m):
            """
            Führt einen Berechnungsschritt auf der Karte durch.
            Parameter: m (list): Die aktuelle Karte.
            """

            changed = False
            out = [row[:] for row in m]
            for y in range(height):
                for x in range(width):
                    cell = m[y][x]
                    if cell == 0:
                        continue

                    if cell == 2 or (isinstance(cell, str) and cell.startswith("F")):
                        prefix = "F"
                    elif cell == 3 or (isinstance(cell, str) and cell.startswith("W")):
                        prefix = "W"
                    elif cell == 1 or (isinstance(cell, str) and cell.startswith("R")):
                        prefix = "R"
                    else:
                        continue

                    top = same_terrain(m[y-1][x] if y > 0 else 0, prefix)
                    right = same_terrain(m[y][x+1] if x < width-1 else 0, prefix)
                    bottom = same_terrain(m[y+1][x] if y < height-1 else 0, prefix)
                    left = same_terrain(m[y][x-1] if x > 0 else 0, prefix)

                    new_code = get_tile_code(prefix, top, right, bottom, left, m, y, x)
                    if new_code != cell:
                        out[y][x] = new_code
                        changed = True
            return out, changed

        # Berechnung + Stabilisierung (3 Durchläufe)
        new_map, _ = compute_once(new_map)
        for _ in range(3):
            new_map, changed = compute_once(new_map)
            if not changed:
                break

        # Zeilenlängen wiederherstellen
        for i, row in enumerate(map_):
            new_map[i] = new_map[i][:len(row)]

        return new_map






    def generateGrass(self):
            """
            Generiert Gras-Sprites basierend auf der aktualisierten Karte.
            Parameter: Keine.
            """
            self.horizontal_segment_counter = -1
            self.vertical_segment_counter = -1
            for row in self.map:
                self.horizontal_segment_counter = -1
                self.vertical_segment_counter += 1
                for elem in row:
                    self.horizontal_segment_counter += 1
                    if elem == 2:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=1))
                    if elem == "Ft":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=2,))
                    if elem == "Fb":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=2, flip=(False, True)))
                    if elem == "Fr":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=0,))
                    if elem == "Fl":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=0, flip=(True, False)))
                    if elem == "Ftr":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=3))
                    if elem == "Ftl":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=3, flip=(True, False)))
                    if elem == "Fbr":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=4, flip = (True, False)))
                    if elem == "Fbl":
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=4))
                    if elem == 0:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=5))
            

            return self.spritegroup
    
    def generateWall(self):
        """
        Generiert Wand-Sprites basierend auf der aktualisierten Wandkarte.
        Parameter: Keine.
        """
        self.horizontal_segment_counter = -1
        self.vertical_segment_counter = -1
        for row in self.map_wall:
            self.horizontal_segment_counter = -1
            self.vertical_segment_counter += 1
            for elem in row:
                self.horizontal_segment_counter += 1

                # Wall (W)
                if elem == 3: self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=0))
                if elem == "Wt": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=6))
                if elem == "Wb": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=6, flip=(False, True)))
                if elem == "Wr": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=1))
                if elem == "Wl": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=2))
                if elem == "Wtr": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=3))
                if elem == "Wtl": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=4))
                if elem == "Wbr": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=3, flip=(False, True)))
                if elem == "Wbl": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=4, flip=(False, True)))
                if elem == "Wic_tl": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(False, True)))
                if elem == "Wic_bl": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(False, False)))
                if elem == "Wic_tr": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(True, True)))
                if elem == "Wic_br": self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(True, False)))

                # Water (R)
                if elem == 1: self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=0))
                if elem == "Rt": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=6))
                if elem == "Rb": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=6, flip=(False, True)))
                if elem == "Rr": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=1))
                if elem == "Rl": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=2))
                if elem == "Rtr": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=3))
                if elem == "Rtl": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=4))
                if elem == "Rbr": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=3, flip=(False, True)))
                if elem == "Rbl": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=4, flip=(False, True)))
                if elem == "Ric_tl": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(False, True)))
                if elem == "Ric_bl": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(False, False)))
                if elem == "Ric_tr": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(True, True)))
                if elem == "Ric_br": self.entitygroup.add(Wall.Water(self.horizontal_segment_counter*64, self.vertical_segment_counter*64, base_sprite=7, flip=(True, False)))
    
    def generateItems(self):
        """
        Generiert die Sammelobjekte auf der Karte.
        Parameter: Keine.
        """
        self.horizontal_segment_counter = -1
        self.vertical_segment_counter = -1
        for row in range(len(self.map_wall)):
            self.horizontal_segment_counter = -1
            self.vertical_segment_counter += 1
            for elem in range(len(self.map_wall[row])):
                self.horizontal_segment_counter += 1
                if self.map_wall[row][elem] == 0:
                    if self.map[row][elem] == 0:
                        if random.randint(0,100) <= 5:
                            if random.randint (0,100) <= 40:
                                self.entitygroup.add(collectable.Rock(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
                            else:
                                self.entitygroup.add(collectable.Stick(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
       

        self.horizontal_segment_counter = -1
        self.vertical_segment_counter = -1
        for row in range(len(self.map_laser)):
                self.horizontal_segment_counter = -1
                self.vertical_segment_counter += 1
                for elem in range(len(self.map_laser[row])):
                    self.horizontal_segment_counter += 1
                    if self.map_laser[row][elem] == 4:
                        self.entitygroup.add(Wall.Laser_v(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
                    if self.map_laser[row][elem] == 5:
                        self.entitygroup.add(Wall.Laser_h(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
                    if self.map_laser[row][elem] == 11:
                        self.entitygroup.add(interactable.Mushroom(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
                    if self.map_laser[row][elem] == 21:
                        self.entitygroup.add(interactable.interactables(self.horizontal_segment_counter * 64,self.vertical_segment_counter * 64, pygame.Rect(0, 0, 64, 64), "topleft", (128,128), r"Engine\Entity_Classes\Sprites_Entity_Classes\CraftingTableAxe.png", True, True, "Axe", "Stick", "Rock", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 10, False]}, "Craft_Axe"))
                    if self.map_laser[row][elem] == 22:
                        self.entitygroup.add(interactable.interactables(self.horizontal_segment_counter * 64,self.vertical_segment_counter * 64, pygame.Rect(0, 0, 64, 64), "topleft", (128,128), r"Engine\Entity_Classes\Sprites_Entity_Classes\CraftingTableTorch.png", True, True, "Torch", "Stick", "Mushroom_juice", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 10, False]}, "Craft_Axe"))
                    if self.map_laser[row][elem] == 23:
                        self.entitygroup.add(interactable.interactables(self.horizontal_segment_counter * 64,self.vertical_segment_counter * 64, pygame.Rect(0, 0, 64, 64), "topleft", (128,128), r"Engine\Entity_Classes\Sprites_Entity_Classes\CraftingTableMap.png", True, True, "Map", "Shell", "Rock", "Stick", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 10, False]}, "Craft_Axe"))
                    if self.map_laser[row][elem] == 24:
                        self.entitygroup.add(interactable.interactables(self.horizontal_segment_counter * 64,self.vertical_segment_counter * 64, pygame.Rect(0, 0, 64, 64), "topleft", (128,128), r"Engine\Entity_Classes\Sprites_Entity_Classes\CarftingTableMirror.png", True, True, "Mirror", "Shell", "Mushroom_juice", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 10, False]}, "Craft_Axe"))
                    if len(str(self.map_laser[row][elem])) == 3:
                        self.entitygroup.add(npc.Turtle(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, width_blocks=int(str(self.map_laser[row][elem])[1]), height_blocks=int(str(self.map_laser[row][elem])[2])))
                    if self.map_laser[row][elem] == 99:
                        print("Generated")
                        self.trigger = pygame.Rect(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, 128, 192)
                        
        return self.trigger

    def generatePrices(self):
        """
        Generiert die Preisschilder und die entsprechenden Items auf der Karte.
        Parameter: Keine.
        """
        item = None
        self.horizontal_segment_counter = -1
        self.vertical_segment_counter = -1
        for row in range(len(self.map_laser)):
                self.horizontal_segment_counter = -1
                self.vertical_segment_counter += 1
                for elem in range(len(self.map_laser[row])):
                    self.horizontal_segment_counter += 1
                    if self.map_laser[row][elem] == 6 or self.map_laser[row][elem] == 7 or self.map_laser[row][elem] == 8:
                        self.item = None
                        self.entitygroup.add(inventory.PriceInventorySlot(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
                        if self.map_laser[row][elem] == 6:
                            item = self.generateItemsIntoSlots("Rock", self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64)
                        if self.map_laser[row][elem] == 7:
                            item = self.generateItemsIntoSlots("Stick", self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64)
                        if self.map_laser[row][elem] == 8:
                            item = self.generateItemsIntoSlots("Mushroom_juice", self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64)
                        if self.map_laser[row][elem] == 9: 
                            item = self.generateItemsIntoSlots("Shell", self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64)
                        if item is not None:
                            self.entitygroup.add(item)
                            item.should_pick_up = False

        return self.entitygroup

    def generateItemsIntoSlots(self, item, pos_x, pos_y):
        """Funktion, die ein Item in ein Preisschild legt
        Parameter: item (str): Name des Items, pos_x (int): x-Position des Items, pos_y (int): y-Position des Items
        """
        if item == "Rock":
            item = collectable.Rock(pos_x, pos_y)
        if item == "Stick":
            item = collectable.Stick(pos_x, pos_y)
        if item == "Mushroom_juice":
            item = collectable.Mushroom_juice(pos_x, pos_y)
        if item == "Shell":
            item = collectable.Shell(pos_x, pos_y)
        return item

        


inventoryCollectables = {}

def dropItemFromInventory():
    """
    Funktion, die das letzte Item aus dem Inventar entfernt und es in der Mitte des Bildschirms spawnt
    Parameter: Keine
    """
    for i in range (len(inventoryCollectables)):
        j = len(inventoryCollectables) - i - 1
        keys = list(inventoryCollectables.keys())
        if keys[j].function == "Item":
            removeItemFromInventory(keys[j].name)
            currentCollectable = getattr(collectable, keys[j].name)
            return currentCollectable((settings.SCREEN_WIDTH)/2, (settings.SCREEN_HEIGHT)/2)

def addItemToInventory(item):
    """
    Funktion, die ein Item ins Inventar hinzufügt
    Parameter: item (Collectable): Das hinzuzufügende Item
    """
    if len(itemField_group) < 7 and item.function == "Item":
        inventoryCollectables[item] = item.name
        return updateInventory()
    if len(toolField_group) < 4 and item.function == "Tool":
        inventoryCollectables[item] = item.name
        return updateInventory()

def removeItemFromInventory(itemName):
    """
    Funktion, die ein Item vom Inventar entfernt
    Parameter: itemName (str): Der Name des zu entfernenden Items
    """
    for elem in inventoryCollectables:
        if elem.name == itemName:
            inventoryCollectables.pop(elem)
            return updateInventory()

def GetNumberOfItems(itemName):
    """
    Funktion, die die Anzahl der Items im Inventar zurückgibt
    Parameter: itemName (str): Der Name des zu zählenden Items"""
    itemcount = -1
    for elem in inventoryCollectables:
        if elem.name == itemName:
            itemcount += 1
    return itemcount
    
def updateInventory():
    """
    Funktion, die das Inventar neu lädt
    Parameter: Keine
    """

    overlayGroup = pygame.sprite.Group()
    inventoryItems = {}
    inventoryTools = {}

    for elem in inventoryCollectables:
        if elem.function == "Item":
            inventoryItems[elem] = inventoryCollectables[elem]
        elif elem.function == "Tool":
            inventoryTools[elem] = inventoryCollectables[elem]
    
    overlayGroup.empty()
    overlayGroup.add(createToolbar(len(inventoryTools), 64, 6, 750), createItembar(len(inventoryItems), 64, 6, 450))

    for i, key in enumerate(list(inventoryItems.keys())):
        if i < len(itemField_group):
            slot = list(itemField_group)[i]
            slot.source = key.source
            slot.update_image()
    for i, key in enumerate(list(inventoryTools.keys())):
        if i < len(toolField_group):    
            slot = list(toolField_group)[i]
            slot.source = key.source
            slot.update_image()

    return overlayGroup


def createItembar(slotCount, slotSize, edgeWidth, yPos):
    """
    Funktion, die ein Inventar für die Items erstellt
    Parameter: slotCount (int): Anzahl der Slots, slotSize (float): Grösse der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, 
    yPos (float): y-Position des Itembars
    """
    global itemField_group
    itemField_group = pygame.sprite.Group()
    slots_group = pygame.sprite.Group()
    slots_group = createInventorySlotsHorizontal(slots_group, slotSize, slotCount, edgeWidth, yPos)
    itemField_group = createInventoryItemFieldsHorizontal(itemField_group, slotSize, slotCount, edgeWidth, yPos)
    return pygame.sprite.Group(slots_group, itemField_group)

def createInventorySlotsHorizontal(slots_group, slotSize, slotCount, edgeWidth, yPos):
    """
    Funktion, die eine Liste von Inventar Slots erstellt und sie nebeneinander platziert \t SlotSize: float für die Grösse des Slots
    Parameter: slots_group (pygame.sprite.Group): Gruppe für die Slots, slotSize (float): Grösse der Slots, slotCount (int): Anzahl der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, yPos (float): y-Position des Itembars
    """
    for i in range(slotCount):
        currentSlotSize = (i)*(slotSize)
        slot = inventory.InventorySlot((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentSlotSize, (settings.SCREEN_WIDTH//2) - yPos, pygame.Rect(0, 0, 64, 64), (slotSize, slotSize), r"InventorySlot.png")
        slots_group.add(slot)
    return pygame.sprite.Group(slots_group)

def createInventoryItemFieldsHorizontal(itemField_group, slotSize, slotCount, edgeWidth, yPos):
    """
    Funktion, die eine Liste von Inventar Felder fürs spätere füllen erstellt und sie in den Item Slots platziert
    Parameter: itemField_group (pygame.sprite.Group): Gruppe für die Item Felder, slotSize (float): Grösse der Slots, slotCount (int): Anzahl der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, yPos (float): y-Position des Itembars
    """
    iconSize = slotSize - 2*edgeWidth
    for i in range(slotCount):
        currentIconSize = i*(slotSize)
        itemField = inventory.InventorySlot((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentIconSize + edgeWidth, (settings.SCREEN_WIDTH//2) + edgeWidth - yPos, pygame.Rect(0, 0, 64, 64), (iconSize, iconSize), r"EmptyIcon.png")
        itemField_group.add(itemField)
    return pygame.sprite.Group(itemField_group)

# Toolbar
def createToolbar(slotCount, slotSize, edgeWidth, yPos):
    """Funktion, die ein Inventar für die Tools erstellt  
    Parameter: slotCount (int): Anzahl der Slots, slotSize (float): Grösse der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, yPos (float): y-Position des Toolbars
    """
    global toolField_group
    toolField_group = pygame.sprite.Group()
    slots_group = pygame.sprite.Group()
    slots_group = createInventorySlotsVertical(slots_group, slotSize, slotCount, edgeWidth, yPos)
    toolField_group = createInventoryToolFieldsVertical(toolField_group, slotSize, slotCount, edgeWidth, yPos)
    return pygame.sprite.Group(slots_group, toolField_group)

def createInventorySlotsVertical(slots_group, slotSize, slotCount, edgeWidth, xPos):
    """Funktion, die eine Liste von Inventar Slots erstellt und sie nebeneinander platziert
    Parameter: slots_group (pygame.sprite.Group): Gruppe für die Slots, slotSize (float): Grösse der Slots, slotCount (int): Anzahl der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, yPos (float): y-Position des Itembars
    """ 
    for i in range(slotCount):
        currentSlotSize = (i)*(slotSize)
        slot = inventory.InventorySlot((settings.SCREEN_HEIGHT//2)/2 + xPos, (settings.SCREEN_HEIGHT//2)-((slotCount/2)*slotSize) + currentSlotSize, pygame.Rect(0, 0, 64, 64), (slotSize, slotSize), r"InventorySlot.png")
        slots_group.add(slot)
    return pygame.sprite.Group(slots_group)

def createInventoryToolFieldsVertical(toolField_group, slotSize, slotCount, edgeWidth, xPos):
    """Funktion, die eine Liste von Inventar Felder fürs spätere füllen erstellt und sie in den Tool Slots platziert
    Parameter: toolField_group (pygame.sprite.Group): Gruppe für die Tool Felder, slotSize (float): Grösse der Slots, slotCount (int): Anzahl der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, xPos (float): x-Position des Toolbars
    """
    iconSize = slotSize - 2*edgeWidth
    for i in range(slotCount):
        currentIconSize = i*(slotSize)
        toolField = inventory.InventorySlot((settings.SCREEN_HEIGHT//2)/2 + edgeWidth  + xPos, (settings.SCREEN_HEIGHT//2)-((slotCount/2)*slotSize) + currentIconSize + edgeWidth, pygame.Rect(0, 0, 64, 64), (iconSize, iconSize), r"EmptyIcon.png")
        toolField_group.add(toolField)
    return pygame.sprite.Group(toolField_group)