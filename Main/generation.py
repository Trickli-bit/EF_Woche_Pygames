import csv
import Engine.Entity_Classes.floor as Floor
import Engine.Entity_Classes.Wall as Wall
import pygame
import Engine.Entity_Classes.inventorySlot as inventory
import Main.settings as settings
import random
import Engine.Entity_Classes.collectable as collectable

class generateLandscape():
    """Liest eine CSV-Datei ein und erstellt eine 2D-Liste der Werte."""
    def __init__(self, spritegroup, entitygroup):
        """ Initialisiert die Klasse mit dem Dateinamen der CSV-Datei.
        param:\t filename (str) - Pfad zur CSV-Datei."""

        self.map = self.readCSV("Main/mapCSV.csv")
        self.map_wall = self.readCSV("Main/mapCSVWall.csv")
        self.spritegroup = spritegroup
        self.entitygroup = entitygroup
        
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
        """Liest die CSV-Datei und erstellt die 2D-Liste der Werte.
        param:\t filename (str) - Pfad zur CSV-Datei."""

        with open(filename, "r") as file:
            print("Öffne Datei:", filename)
            reader = csv.reader(file)
            data = [list(map(int, row)) for row in reader]

        return data
    
    def update_tiles(self, map_):
        height = len(map_)-2
        width = max((len(r) for r in map_), default=0)

        full = [row[:] + [0] * (width - len(row)) for row in map_]
        new_map = [row[:] for row in full]

        neigh8 = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

        def same_terrain(val, prefix):
            if prefix == "F":
                return val == 2 or (isinstance(val, str) and val.startswith("F"))
            else:
                return val == 3 or (isinstance(val, str) and val.startswith("W"))

        # Phase 1: F/W auf 0er Felder propagieren
        for y in range(height):
            for x in range(width):
                v = full[y][x]
                if v == 2 or v == 3:
                    p = "F" if v == 2 else "W"
                    for dy, dx in neigh8:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width and full[ny][nx] == 0:
                            new_map[ny][nx] = p

        # Tile-Code bestimmen
        def get_tile_code(prefix, top, right, bottom, left, m, y, x):
            def diag(dy, dx):
                ny, nx = y+dy, x+dx
                return 0 <= ny < len(m) and 0 <= nx < len(m[0]) and same_terrain(m[ny][nx], prefix)

            top_left = diag(-1,-1)
            top_right = diag(-1,1)
            bottom_left = diag(1,-1)
            bottom_right = diag(1,1)

            # Normale äußere Ecken
            if not top and not right: return prefix + "tr"
            if not top and not left:  return prefix + "tl"
            if not bottom and not right: return prefix + "br"
            if not bottom and not left:  return prefix + "bl"

            # Innere Ecken nur für W
            if prefix == "W":
                if top and left and not top_left: return "Wic_tl"
                if top and right and not top_right: return "Wic_tr"
                if bottom and left and not bottom_left: return "Wic_bl"
                if bottom and right and not bottom_right: return "Wic_br"

            # Kanten
            if not top: return prefix + "t"
            if not right: return prefix + "r"
            if not bottom: return prefix + "b"
            if not left: return prefix + "l"

            # Innenbereich
            return 2 if prefix == "F" else 3

        def compute_once(m):
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
                    else:
                        continue

                    top    = same_terrain(m[y-1][x] if y > 0 else 0, prefix)
                    right  = same_terrain(m[y][x+1] if x < width-1 else 0, prefix)
                    bottom = same_terrain(m[y+1][x] if y < height-1 else 0, prefix)
                    left   = same_terrain(m[y][x-1] if x > 0 else 0, prefix)

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

        print(new_map)

        return new_map





    def generateGrass(self):
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
            self.horizontal_segment_counter = -1
            self.vertical_segment_counter = -1
            for row in self.map_wall:
                self.horizontal_segment_counter = -1
                self.vertical_segment_counter += 1
                for elem in row:
                    self.horizontal_segment_counter += 1
                    if elem == 3:
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=0))
                    if elem == "Wt":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=6))
                    if elem == "Wb":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=6, flip = (False, True)))
                    if elem == "Wr":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=1))
                    if elem == "Wl":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=2))
                    if elem == "Wtr":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=3))
                    if elem == "Wtl":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=4))
                    if elem == "Wbr":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=3, flip=(False, True)))
                    if elem == "Wbl":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=4, flip = (False, True)))
                    if elem == "Wic_tl":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=7, flip = (False, True)))
                    if elem == "Wic_bl":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=7, flip = (False, False)))
                    if elem == "Wic_tr":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=7, flip = (True, True)))
                    if elem == "Wic_br":
                        self.entitygroup.add(Wall.Wall(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=7, flip = (True, False)))

            return self.entitygroup
    

    
    def generateItems(self):
        a = []
        print("generate STICK AND ROCKS")
        self.horizontal_segment_counter = -1
        self.vertical_segment_counter = -1
        print("THIS IS", self.map_wall)
        for row in range(len(self.map_wall)):
            self.horizontal_segment_counter = -1
            self.vertical_segment_counter += 1
            for elem in range(len(self.map_wall[row])):
                self.horizontal_segment_counter += 1
                if self.map_wall[row][elem] == 0:
                    if self.map[row][elem] == 0:
                        if random.randint(0,100) <= 5:
                            if random.randint (0,100) <= 20:
                                print("generate Rock", self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64)
                                a.append(collectable.Rock(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))
                            else:
                                print("generate Stick", self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64)
                                a.append(collectable.Stick(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64))

        return a



inventoryItems = {}

def addItemToInventory(item):
    """Funktion, die ein Item dem Inventar hinzufügt"""
    inventoryItems[item.name] = item.source
    return updateToolbar()

def removeItemFromInventory(itemName):
    """Funktion, die ein Item vom Inventar entfernt"""
    for elem in inventoryItems:
        if elem == itemName:
            inventoryItems.pop(itemName)
            return updateToolbar()

def GetNumberOfItems(itemName):
    """Funktion, die die Anzahl der Items im Inventar zurückgibt"""
    itemcount = -1
    for elem in inventoryItems:
        if elem == itemName:
            itemcount += 1
    return itemcount
    
def updateToolbar():
    """Funktion, die die Toolbar aktualisiert"""
    overlayGroup = pygame.sprite.Group()
    overlayGroup = createToolbar(len(inventoryItems), 64, 6, 450)
    for i, value in enumerate(list(inventoryItems.values())):
        slot = list(itemField_group)[i]
        slot.source = value
        slot.update_image()
    return overlayGroup

def createToolbar(slotCount, slotSize, edgeWidth, yPos):
    """Funktion, die eine Toolbar erstellt"""
    global itemField_group
    itemField_group = pygame.sprite.Group()
    slots_group = pygame.sprite.Group()
    slots_group = createInventorySlots(slots_group, slotSize, slotCount, edgeWidth, yPos)
    itemField_group = createInventoryItemFields(itemField_group, slotSize, slotCount, edgeWidth, yPos)
    return pygame.sprite.Group(slots_group, itemField_group)

def createInventorySlots(slots_group, slotSize, slotCount, edgeWidth, yPos):
    """Funktion, die eine Liste von Inventar Slots erstellt und sie nebeneinander platziert \t SlotSize: float für die Grösse des Slots"""
    for i in range(slotCount):
        currentSlotSize = (i)*(slotSize)
        slot = inventory.InventorySlot((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentSlotSize, (settings.SCREEN_WIDTH//2) - yPos, pygame.Rect(0, 0, 64, 64), (slotSize, slotSize), r"InventorySlot.png")
        slots_group.add(slot)
    return pygame.sprite.Group(slots_group)

def createInventoryItemFields(itemField_group, slotSize, slotCount, edgeWidth, yPos):
    """Funktion, die eine Liste von Inventar Felder fürs spätere füllen erstellt und sie in den Item Slots platziert"""
    iconSize = slotSize - 2*edgeWidth
    for i in range(slotCount):
        currentIconSize = i*(slotSize)
        itemField = inventory.InventorySlot((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentIconSize + edgeWidth, (settings.SCREEN_WIDTH//2) + edgeWidth - yPos, pygame.Rect(0, 0, 64, 64), (iconSize, iconSize), r"EmptyIcon.png")
        itemField_group.add(itemField)
    return pygame.sprite.Group(itemField_group)
