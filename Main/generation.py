import pygame
import Engine.Entity_Classes.inventorySlot as inventory
import Main.settings as settings


def createInventorySlots(slots_group, items_group, slotSize, slotCount, edgeWidth):
    """Funktion, die eine Liste von Inventar Slots erstellt und sie nebeneinander platziert \t SlotSize: float für die Grösse des Slots"""
    iconSize = slotSize - edgeWidth/100
    for i in range(slotCount):
        currentSlotSize = i*(slotSize-edgeWidth)
        currentIconSize = i*(iconSize-edgeWidth)
        slot = inventory.InventorySlot((settings.SCREEN_WIDTH//2)-((slotCount/2)*slotSize) + currentSlotSize, (settings.SCREEN_WIDTH//2) + 2*slotSize, pygame.Rect(0, 0, slotSize, slotSize), (slotSize, slotSize), r"Wall.png")
        itemField = inventory.InventorySlot((settings.SCREEN_WIDTH//2)-((slotCount/2)*iconSize) + currentIconSize, (settings.SCREEN_WIDTH//2) + 2*iconSize, pygame.Rect(0, 0, iconSize, iconSize), (iconSize, iconSize), r"Icon.png")
        slots_group.add(slot)
        items_group.add(itemField)
    return pygame.sprite.Group(slots_group, items_group)