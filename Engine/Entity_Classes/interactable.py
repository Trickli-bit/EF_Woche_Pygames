import pygame
import Engine.entities as entities

placeholderitem = True
"""Platzhalter für eine Überprüfung, ob das Invertar ein oder mehrere Items hat"""
def placeholderfunction1(item):
    print("hi")
"""Platzhalter für eine Funktion, die Items aus dem Inventar entfernt"""
def placeholderfunction2(item):
    print("hu")
    """Platzhalter für eine Funktion, die Items dem augibt"""

class interactables(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, output, input1 = "air", input2 = "air", input3 = "air", input4 = "air", fix = True, base_sprite = 0, ani_frames_count = 0, ani_animations = {}, ani_name = ""):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3
        self.input4 = input4
        self.output = output
        self.ani_name = ani_name

        """Klasse zur Erstellung von Obiekten mit einer Funktion (Für das Crafting System)
        param: \t pos_x (int), pos_y, (int) (pos_x = 0, pos_y = 0, breite, höhe) Rechteck_attachment (str), Skalierung (int), Pfad (r-str),  Solid? (boolean), Ist_SpriteSheet? (boolean), Resultat(item id), input1-4(item id),  Basis Sprite (int), Anz. Frames (int), Animationen in einem Dict mit {"Animationsname" : [1. Frame, letztes Frame, geschwindigkeit, loop (bolean)]}"""
    def interact(self):
        """Aktiviert beim nahe sein. nimmt items aus dem Inventory und gibt ein Resultat zurück"""
        if self.input4 == "air":
            if self.input3 == "air":
                if self.input2 == "air":
                    if placeholderitem == True:
                        placeholderfunction1(self.input1)
                        self.Animation.start_animation(self.ani_name)
                        placeholderfunction2(self.output)
                else:
                    if placeholderitem == True:
                        placeholderfunction1(self.input1)
                        placeholderfunction1(self.input2)
                        self.Animation.start_animation(self.ani_name)
                        placeholderfunction2(self.output)
            else:
                if placeholderitem == True:
                    placeholderfunction1(self.input1)
                    placeholderfunction1(self.input2)
                    placeholderfunction1(self.input3)
                    self.Animation.start_animation(self.ani_name)
                    placeholderfunction2(self.output)
                        
        else:
            if placeholderitem == True:
                placeholderfunction1(self.input1)
                placeholderfunction1(self.input2)
                placeholderfunction1(self.input3)
                placeholderfunction1(self.input4)
                self.Animation.start_animation(self.ani_name)
                placeholderfunction2(self.output)

class resources(entities.Entity):
    def __init__(self, pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, drop = "air", fix = True, base_sprite = 0, ani_frames_count = 0, ani_animations = {}, ani_name = ""):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        self.drop = drop
        self.ani_name = ani_name
        """Klasse zur Erstellung von Ressourcen (Können abgebaut werden und geben ein Item zurück)"""
    def harvest(self):
        """Aktivierung durch knopfdruck. Gibt ein Item zurück und startet eine Animation"""
        if placeholderitem:
            self.Animation.start_animation(self.ani_name)
            placeholderfunction2(self.drop)

#Axecrafter = interactables(0, 0, pygame.Rect(0, 0, 64, 64), "topleft", (64,64), r"Engine\Entity_Classes\Sprites_Entity_Classes\pixilart-sprite (6).png", True, False, "Axe", "stick", "stone", "air", "air", False, 0, 8, {"Craft_Axe" : [0, 7, 5, False]})