import Engine.Entity_Classes.collectable  as collectable

class Collision:
    """Kollisionsklasse, die Kollisionen zwischen Objekten behandelt."""
    def __init__(self, entities, movable_entities, player):
        """ Initialisiert die Kollisionsklasse mit festen und beweglichen Entitäten. 
        param:\t entities (pygame.sprite.Group) - Gruppe der festen Entitäten"""
        self.entity_group = entities  # args is a sequence of objects
        self.movable_entities = movable_entities
        self.player = player

    def collide_with_solid(self, other):
        """ Überprüft und behandelt Kollisionen zwischen einer beweglichen Entität und festen Objekten.
        param:\t other (EntityMovable) - die bewegliche Entität, die überprüft werden soll."""
        for entity in self.entity_group:
            if entity.solid and other.rect.colliderect(entity.rect):
                other.collition(entity.rect.x , entity.rect.y)
    


    def update(self):
        """ Aktualisiert die Kollisionen für alle beweglichen Entitäten."""
        for movable in self.movable_entities:
            self.collide_with_solid(movable)

        for entity in self.entity_group:
            if self.player.rect.colliderect(entity.rect):
                self.collide_with_collectable(entity)
