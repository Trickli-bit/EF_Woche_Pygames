import Engine.entities as entities
import Main.events
import Main.generation as generation
import pygame
import Player.player as player
import Engine.Entity_Classes.animations as animations 
import Main.events as events
import Main.sounds as sounds

"""
Basisklasse für sammelbare Objekte im Spiel
"""
class Collectable(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach,
                 scale=(64,64), source=None, solid=False, is_spritesheet=False,
                 fix=False, base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.value = 0
        self.collected = False
        self.pick_up = None
        self.source = source
        self.function = "Item"
        self.craftable = False
        self.should_pick_up = True

   
    def collide_with_player(self, player_obj):
        """
        Eine Funktion die prüft, ob der Spieler das Collectable berührt und fügt es dem Inventar hinzu.
        Parameter: player_obj - das Spielerobjekt, mit dem die Kollision überprüft wird
        """
        if self.should_pick_up and sum(1 for elem in generation.inventoryCollectables if elem.function == "Item") < 7:
            """
            Prüft, ob der Spieler das Collectable berührt.
            Nur wenn die Rechtecke überlappen und das Objekt noch nicht gesammelt wurde.
            Falls schon gesammelt, nichts tun
            """
            if self.collected:
                pass
                return
            """
            Parameter: player_obj - das Spielerobjekt, mit dem die Kollision überprüft wird
            """
            if not isinstance(player_obj, player.Player):
                pass
                #return  # Nur Player kann sammeln

            """
            Parameter: player_obj - das Spielerobjekt, mit dem die Kollision überprüft wird
            """
            if not isinstance(player_obj, player.Player):
                pass
                #return  # Nur Player kann sammeln

            """
            Parameter: player_obj - das Spielerobjekt, mit dem die Kollision überprüft wird
            """
            if self.rect.colliderect(player_obj.rect):
                self.collected = True
                """
                Sound für das aufsammeln von Items 
                """
                sounds.play_bubble_pop()
                """
                 Die drei Zeilen fügen das Item ins Inventar des Spielers ein, 
                 erstellen an seiner Position eine Aufheb-Animation und lassen diese im Spiel ablaufen.   
                """
                player_obj.item_dict[self.name] = player_obj.item_dict.get(self.name, 0) + self.value
                self.pick_up = animations.pick_up_animation(self.rect.centerx, self.rect.centery)
                events.checkAnimations(self.pick_up)



                """
                Entfernt das Objekt aus der aktuellen Gruppe und entfernt das dazugehörige Sprite.
                """
                self.kill()
                return generation.addItemToInventory(self)

    """ Fügt das Collectable einer angegebenen Gruppe hinzu.
    Parameter: gruppe - die Gruppe, der das Collectable hinzugefügt werden soll
    """  
    def zur_gruppe_hinzufuegen(self, gruppe):
            gruppe.add(self)

    """ Aktualisiert die Position des Collectables basierend auf den übergebenen Verschiebungswerten.
    Parameter: dx - Verschiebung in x-Richtung
               dy - Verschiebung in y-Richtung  
    """
    def update(self, dx = 0, dy = 0, keys = []):
        super().update(dx, dy, keys)    

        """     
        Verschiedene sammelbare Objekte, die von der Collectable-Klasse erben 
        Parameter: pos_x - x-Position des Objekts
        pos_y - y-Position des Objekts
        rect - Rechteck für die Kollisionserkennung
           """
class Stick(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\stock-pixilart (2).png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        """
        Gibt dem Objekt spezifische Eigenschaften wie Name, Funktion, ob es craftbar ist und seinen Wert.
        """
        self.name = "Stick"
        self.function = "Item"
        self.craftable = False
        self.value = 1

        """ 
        Eine weitere sammelbare Objektklasse
        """

class Rock(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\stein-pixilart (5).png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Rock"
        self.function = "Item"
        self.craftable = False
        self.value = 1

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """

class Mushroom_juice(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\mushroo_juice.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Mushroom_juice"
        self.function = "Item"
        self.craftable = False
        self.value = 1   

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """
class Shell(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Shell.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Shell"
        self.function = "Item"
        self.craftable = False
        self.value = 1

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """
class Axe(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Axe.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Axe"
        self.function = "Tool"
        self.craftable = True
        self.value = 1

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """
class Map(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Map.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Map"
        self.function = "Tool"
        self.craftable = True
        self.value = 1

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """
class Mirror(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Mirror.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Mirror"
        self.function = "Item"
        self.craftable = True
        self.value = 1

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """
class Torch(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Torch.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "Torch"
        self.function = "Tool"
        self.craftable = True
        self.value = 1

        """
        Noch eine sammelbare Objektklasse mit der Vererbung von Collectable
        """
class RecipeBook(Collectable):
    def __init__(self, pos_x, pos_y, rect=pygame.Rect(0,0,64,64), rect_attach="topleft",
                 scale=(64,64), source=r"Engine\Entity_Classes\Sprites_Entity_Classes\RecipeBook.png",
                 solid=False, is_spritesheet=False, fix=False,
                 base_sprite=0, ani_frames_count=0, ani_animations={}):
        super().__init__(
            pos_x=pos_x, pos_y=pos_y, rect=rect, rect_attach=rect_attach,
            scale=scale, source=source, solid=solid, is_spritesheet=is_spritesheet,
            fix=fix, base_sprite=base_sprite, ani_frames_count=ani_frames_count,
            ani_animations=ani_animations
        )
        self.name = "RecipeBook"
        self.function = "Tool"
        self.craftable = False
        self.value = 1