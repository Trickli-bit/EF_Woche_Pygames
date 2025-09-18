import pygame
import Main.settings as settings
import Engine.Entity_Classes.Interface as interface
import Engine.Entity_Classes.collectable as collectable


inventoryCollectables = {}

def fullInventory():
    """Funktion, die überprüft, ob das Inventar voll ist"""
    return sum(elem.value for elem in inventoryCollectables if elem.function == "Item") >= 7

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
        slot = interface.Interface((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentSlotSize, (settings.SCREEN_WIDTH//2) - yPos, pygame.Rect(0, 0, 64, 64), (slotSize, slotSize), r"Sprites_Main/InventorySlot.png")
        slots_group.add(slot)
    if fullInventory():
        redPoint = interface.Interface((settings.SCREEN_WIDTH//2)+(7/2)*64, (settings.SCREEN_WIDTH//2)-440, pygame.Rect(0, 0, 64, 64), (40, 40), r"Sprites_Main\QRedSign.png")
        slots_group.add(redPoint)
    return pygame.sprite.Group(slots_group)

def createInventoryItemFieldsHorizontal(itemField_group, slotSize, slotCount, edgeWidth, yPos):
    """
    Funktion, die eine Liste von Inventar Felder fürs spätere füllen erstellt und sie in den Item Slots platziert
    Parameter: itemField_group (pygame.sprite.Group): Gruppe für die Item Felder, slotSize (float): Grösse der Slots, slotCount (int): Anzahl der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, yPos (float): y-Position des Itembars
    """
    iconSize = slotSize - 2*edgeWidth
    for i in range(slotCount):
        currentIconSize = i*(slotSize)
        itemField = interface.Interface((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentIconSize + edgeWidth, (settings.SCREEN_WIDTH//2) + edgeWidth - yPos, pygame.Rect(0, 0, 64, 64), (iconSize, iconSize), r"Sprites_Main/EmptyIcon.png")
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
        slot = interface.Interface((settings.SCREEN_HEIGHT//2)/2 + xPos, (settings.SCREEN_HEIGHT//2)-((slotCount/2)*slotSize) + currentSlotSize, pygame.Rect(0, 0, 64, 64), (slotSize, slotSize), r"Sprites_Main/InventorySlot.png")
        slots_group.add(slot)
    return pygame.sprite.Group(slots_group)

def createInventoryToolFieldsVertical(toolField_group, slotSize, slotCount, edgeWidth, xPos):
    """Funktion, die eine Liste von Inventar Felder fürs spätere füllen erstellt und sie in den Tool Slots platziert
    Parameter: toolField_group (pygame.sprite.Group): Gruppe für die Tool Felder, slotSize (float): Grösse der Slots, slotCount (int): Anzahl der Slots, edgeWidth (float): Abstand des Icons zum Slot-Rand, xPos (float): x-Position des Toolbars
    """
    iconSize = slotSize - 2*edgeWidth
    for i in range(slotCount):
        currentIconSize = i*(slotSize)
        toolField = interface.Interface((settings.SCREEN_HEIGHT//2)/2 + edgeWidth  + xPos, (settings.SCREEN_HEIGHT//2)-((slotCount/2)*slotSize) + currentIconSize + edgeWidth, pygame.Rect(0, 0, 64, 64), (iconSize, iconSize), r"Sprites_Main/EmptyIcon.png")
        toolField_group.add(toolField)
    return pygame.sprite.Group(toolField_group)