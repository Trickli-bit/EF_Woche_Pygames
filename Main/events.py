import pygame
import Engine.Entity_Classes.collectable as collectable
import Player.player as player
import Engine.Entity_Classes.npc as npc
import Engine.Entity_Classes.inventorySlot as inventory
import pygame
import Engine.Entity_Classes.Wall as wall
import Engine.Entity_Classes.interactable as interactable
import Main.sounds as sounds


class Collision:
    """
    Kollisionsklasse für feste und bewegliche Objekte.
    Parameter:
    entities (pygame.sprite.Group): Gruppe aller festen Objekte.
    movable_entities (pygame.sprite.Group): Gruppe aller beweglichen Objekte.
    playerGroup (pygame.sprite.Group): Gruppe aller Spieler-Objekte.
    """

    def __init__(self, entities, movable_entities, playerGroup):
        """Initialisiert die Kollisionsklasse mit den gegebenen Gruppen.

        Parameter:
        entities (pygame.sprite.Group): Gruppe aller festen Objekte.
        movable_entities (pygame.sprite.Group): Gruppe aller beweglichen Objekte.
        playerGroup (pygame.sprite.Group): Gruppe aller Spieler-Objekte.
        """
        self.objects = entities
        self.movable_entities = movable_entities
        self.playerGroup = playerGroup

    def collide_with_solid(self, other):
        """
        Überprüft Kollisionsrichtung für ein einzelnes bewegliches Objekt.   
        Parameter: other (MovableEntity): Das bewegliche Objekt, das überprüft wird.
        """
        collision_offset = 16
        coll_rect = other.rect.inflate(-collision_offset*2, -collision_offset*2)
        collided = False
        for entity in self.objects:
            if entity.solid:
                entity_rect = entity.rect.inflate(-collision_offset*2, -collision_offset*2)
                if coll_rect.colliderect(entity_rect):
                    other.collition(entity)
                    collided = True
                    break
        if not collided:
            other.solid_collision_direction = None

    def collition_with_collectable(self):
        """
        Überprüft Kollisionen zwischen dem Spieler und sammelbaren Objekten.
        Wenn eine Kollision erkannt wird, wird die entsprechende Methode des sammelbaren Objekts aufgerufen.
        """
        for entity in self.objects:
            if isinstance(entity, collectable.Collectable):
                for player in self.playerGroup:
                    entity.collide_with_player(player)
                    
            if isinstance(entity, npc.Turtle):
                for player in self.playerGroup:
                    if player.rect.colliderect(entity.rect):
                        player.ready_to_attack = True
                        player.attaking_objects.append(entity)

            if isinstance(entity, interactable.Mushroom):
                for player in self.playerGroup:
                    if player.rect.colliderect(entity.rect):
                        player.ready_to_attack = True
                        player.attaking_objects.append(entity)

            if isinstance(entity, wall.Laser_h) or isinstance(entity, wall.Laser_v):
                for player in self.playerGroup:
                    if player.rect.colliderect(entity.rect):
                        entity.die(self.objects)

            if isinstance(entity, interactable.interactables):
                for player in self.playerGroup:
                    if player.rect.colliderect(entity.rect) and entity.has_tool == False:
                        entity.interact()


    def move_out(self, other):
        """
        Bewegt ein Objekt aus einer Kollision heraus.   
        Parameter: other (MovableEntity): Das bewegliche Objekt, das bewegt wird.
        """
        move_amount = 16
        if other.solid_collision_direction == "up":
            other.dy += move_amount
        elif other.solid_collision_direction == "down":
            other.dy -= move_amount
        elif other.solid_collision_direction == "right":
            other.dx -= move_amount
        elif other.solid_collision_direction == "left":
            other.dx += move_amount
        elif other.solid_collision_direction == "leftup":
            other.dx -= move_amount
            other.dy -= move_amount
        elif other.solid_collision_direction == "leftdown":
            other.dx += move_amount
            other.dy -= move_amount
        elif other.solid_collision_direction == "rightup":
            other.dx -= move_amount
            other.dy += move_amount
        elif other.solid_collision_direction == "rightdown":
            other.dx += move_amount
            other.dy += move_amount


    def update(self):
        """
        Aktualisiert alle Kollisionen für Movable Entities und Player.   
        Ruft die entsprechenden Methoden auf, um Kollisionen zu überprüfen und Objekte zu bewegen.
        """
        for movable in self.movable_entities:
            self.collide_with_solid(movable)
        for player in self.playerGroup:
            self.collide_with_solid(player)
        for player in self.playerGroup:
            if hasattr(player, "rect"):
                self.collition_with_collectable()
        for player in self.playerGroup:
            self.move_out(player)
        for movable in self.movable_entities:
            self.move_out(movable)

animation_to_add = None

def checkAnimations(animation):
    """
    Überprüft die Animationen für ein bestimmtes Objekt.
    Parameter: animation (pygame.sprite.Sprite): Das Objekt, dessen Animation überprüft wird.
    """
    global animation_to_add
    animation_to_add = animation
    addingAnimation()
    

def addingAnimation():
    """
    Fügt die Animation zur Liste der Animationen hinzu.
    Rückgabe: pygame.sprite.Sprite oder None: Die hinzugefügte Animation oder None, wenn keine vorhanden ist.
    """
    global animation_to_add
    return animation_to_add