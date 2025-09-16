
class Collision:
    """Kollisionsklasse für feste und bewegliche Objekte."""

    def __init__(self, entities, movable_entities, playerGroup):
        self.objects = entities
        self.movable_entities = movable_entities
        self.playerGroup = playerGroup

    def collide_with_solid(self, other):
        """Überprüft Kollisionsrichtung für ein einzelnes bewegliches Objekt."""
        other.solid_collision_direction = None
        collision_offset = 16
        coll_rect = other.rect.inflate(-collision_offset*2, -collision_offset*2)
        for entity in self.objects:
            if entity.solid:
                entity_rect = entity.rect.inflate(-collision_offset*2, -collision_offset*2)
                if coll_rect.colliderect(entity_rect):
                    other.collition(entity)
                    break

    def update(self):
        """Aktualisiert alle Kollisionen für Movable Entities und Player."""
        for movable in self.movable_entities:
            self.collide_with_solid(movable)
        for player in self.playerGroup:
            self.collide_with_solid(player)

animation_to_add = None

def checkAnimations(animation):
    global animation_to_add
    animation_to_add = animation
    addingAnimation()
    

def addingAnimation():
    global animation_to_add
    return animation_to_add