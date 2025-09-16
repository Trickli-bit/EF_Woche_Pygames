import csv
import Engine.Entity_Classes.floor as Floor
import Engine.Entity_Classes.Wall as Wall

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

    def update_tiles(self, map):
        """Ersetzt die grass-Zellen basierend auf Nachbarzellen. MADE BY COPILOT"""
        height = len(self.map) -4
        width = len(self.map[0]) if height > 0 else 0  

        # Priorität: Je niedriger die Zahl, desto 'härter' der Übergang
        # 5–8 sind Ecken, 1–4 Kanten


        # Bewegungsrichtungen für Nachbarn
        transitions = [
            (1, 0),    # unten
            (0, 1),    # rechts
            (-1, 0),   # oben
            (0, -1),   # links
            (1, 1),    # unten-rechts
            (-1, -1),  # oben-links
            (1, -1),   # unten-links
            (-1, 1)    # oben-rechts
        ]

        transitions_dict = {
            (1, 0): "t",
            (0, 1): "l",
            (-1, 0): "b",
            (0, -1): "r",
            (1, 1): "tl",
            (-1, -1): "br",
            (1, -1): "tr",
            (-1, 1): "bl"
        }

     

        # Neue Map erstellen
        new_map = [row[:] for row in map]

        print(new_map)
                                
        for y in range(height): 
            for x in range(width): 
                if map[y][x] == 2 or map[y][x] == 3: 
                    for (dy, dx) in transitions: 
                        ny, nx = y + dy, x + dx 
                        if 0 <= ny < height and 0 <= nx < width :
                            if map[ny][nx] == 0: 
                                if map[y][x] == 2:
                                    new_map[ny][nx] = "F"
                                if map[y][x] == 3:
                                    print("WWWWWWWWWWWWWWWW")
                                    new_map[ny][nx] = "W"


        print(new_map)


        for y in range(height):
            for x in range(width):
                if new_map[y][x] == "F" or new_map[y][x] == "W":
                    for (dy, dx), mark in transitions_dict.items():
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if new_map[ny][nx] == 2 or new_map[ny][nx] == 3:
                                if new_map[y][x] == "F":
                                    new_map[y][x] = "F" + mark
                                if new_map[y][x] == "W":
                                    new_map[y][x] = "W" + mark

        print(new_map)




        for y in range(height):
            for x in range(width):
                if new_map[y][x] == "w":
                    for (dy, dx), mark in transitions_dict.items():
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if new_map[ny][nx] == 3:
                                new_map[y][x] = "3" + mark


        map = new_map
        return map

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
                        print("WALL")
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
            

            return self.entitygroup