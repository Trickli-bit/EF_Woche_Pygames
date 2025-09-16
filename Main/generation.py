import pygame
import Engine.Entity_Classes.inventorySlot as inventory
import Main.settings as settings

def addItemToInventory(item):
    """Funktion, die ein Item dem Inventar hinzufügt"""
    for elem in itemField_group:
        if elem.source == item.source:
            elem.value += 1
            updateItemCount(elem, elem.value)
            break
    for elem in itemField_group:
        if elem.source == r"EmptyIcon.png":
            fillSlotWithItem(elem, item)
            updateItemCount(elem, 1)
            break

def updateItemCount(slot, itemCount):
    """Funktion, die die Anzahl der Items in einem Slot aktualisiert und anzeigt"""
    slot.value = itemCount

def fillSlotWithItem(slot, item):
    """Funktion, die ein Item in einen Slot füllt"""
    slot.source = item.source
    slot.update_image()


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