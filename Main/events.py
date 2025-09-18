import pygame
import Engine.Entity_Classes.collectable as collectable
import Player.player as player
import Engine.Entity_Classes.npc as npc
import Engine.Entity_Classes.inventorySlot as inventory
import pygame
import Engine.Entity_Classes.Wall as wall


class Collision:
    """Kollisionsklasse für feste und bewegliche Objekte."""

    def __init__(self, entities, movable_entities, playerGroup):
        self.objects = entities
        self.movable_entities = movable_entities
        self.playerGroup = playerGroup

    def collide_with_solid(self, other):
        """Überprüft Kollisionsrichtung für ein einzelnes bewegliches Objekt."""
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
        for entity in self.objects:
            if isinstance(entity, collectable.Collectable):
                for player in self.playerGroup:
                    entity.collide_with_player(player)
                    
            if isinstance(entity, npc.Turtle):
                for player in self.playerGroup:
                    if player.rect.colliderect(entity.rect):
                        player.ready_to_attack = True
                        player.attaking_objects.append(entity)

            if isinstance(entity, wall.Laser_h) or isinstance(entity, wall.Laser_v):
                if player.rect.colliderect(entity.rect):
                    entity.die(self.objects)


    def move_out(self, other):
        print(other.solid_collision_direction)
        """Bewegt ein Objekt aus einer Kollision heraus."""
        if other.solid_collision_direction == "up":
            other.dy += 1
        elif other.solid_collision_direction == "down":
            other.dy -= 1
        elif other.solid_collision_direction == "right":
            other.dx -= 1
        elif other.solid_collision_direction == "left":
            other.dx += 1        
        elif other.solid_collision_direction == "leftup":
            other.dx -= 1
            other.dy -= 1
        elif other.solid_collision_direction == "leftdown":
            other.dx += 1
            other.dy -= 1
        elif other.solid_collision_direction == "rightup":
            other.dx -= 1
            other.dy += 1
        elif other.solid_collision_direction == "rightdown":
            other.dx += 1
            other.dy += 1


    def update(self):
        """Aktualisiert alle Kollisionen für Movable Entities und Player."""
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
    global animation_to_add
    animation_to_add = animation
    addingAnimation()
    

def addingAnimation():
    global animation_to_add
    return animation_to_add