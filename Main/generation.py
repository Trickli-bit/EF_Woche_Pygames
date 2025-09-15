import csv
import Engine.Entity_Classes.floor as Floor

class generateLandscape():
    """Liest eine CSV-Datei ein und erstellt eine 2D-Liste der Werte."""
    def __init__(self, spritegroup):
        filename = "Main/mapCSV.csv"
        """ Initialisiert die Klasse mit dem Dateinamen der CSV-Datei.
        param:\t filename (str) - Pfad zur CSV-Datei."""

        self.map = self.readCSV(filename)
        self.spritegroup = spritegroup
        
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

        self.update_grass_tiles()

    def readCSV(self, filename):
        """Liest die CSV-Datei und erstellt die 2D-Liste der Werte.
        param:\t filename (str) - Pfad zur CSV-Datei."""

        with open(filename, "r") as file:
            print("Öffne Datei:", filename)
            reader = csv.reader(file)
            data = [list(map(int, row)) for row in reader]

        return data

    def update_grass_tiles(self):
        """Ersetzt die grass-Zellen basierend auf Nachbarzellen. MADE BY COPILOT"""
        rows = len(self.map)
        cols = len(self.map[0])

        # Kopie der Daten erstellen, damit wir nicht mitten im Update falsche Nachbarn sehen
        new_map = [row[:] for row in self.map]

        for i in range(rows):
            for j in range(cols):
                if self.map[i][j] == 0:  # grass
                    # Nachbarn prüfen (mit Randprüfung)
                    top = self.map[i-1][j] if i > 0 else None
                    bottom = self.map[i+1][j] if i < rows-1 else None
                    left = self.map[i][j-1] if j > 0 else None
                    right = self.map[i][j+1] if j < cols-1 else None

                    # Regeln für potsoile-Nachbarn
                    if right == 9:
                        new_map[i][j] = 2  # grass_r_potsoile
                    if left == 9:
                        new_map[i][j] = 1  # grass_l_potsoile
                    if top == 9:
                        new_map[i][j] = 3  # grass_t_potsoile
                    if bottom == 9:
                        new_map[i][j] = 4  # grass_b_potsoile

                    # Ecken prüfen (Beispiel: oben links)
                    if top == 9 and left == 9:
                        new_map[i][j] = 5  # grass_tl_potsoile
                    if top == 9 and right == 9:
                        new_map[i][j] = 6  # grass_tr_potsoile
                    if bottom == 9 and left == 9:
                        new_map[i][j] = 7  # grass_bl_potsoile
                    if bottom == 9 and right == 9:
                        new_map[i][j] = 8  # grass_br_potsoile

        self.map = new_map
        
    def generateElements(self):
            self.horizontal_segment_counter = -1
            self.vertical_segment_counter = -1
            for row in self.map:
                self.horizontal_segment_counter = -1
                self.vertical_segment_counter += 1
                for elem in row:
                    self.horizontal_segment_counter += 1
                    if elem == 0:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=0))
                    if elem == 1:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=1, flip=True))
                    if elem == 2:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=1))
                    if elem == 3:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=4))
                    if elem == 4:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=4, flip=True))
                    if elem == 5:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=3))
                    if elem == 6:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=3, flip=True))
                    if elem == 7:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=2, flip=True))
                    if elem == 8:
                        self.spritegroup.add(Floor.Grass(self.horizontal_segment_counter * 64, self.vertical_segment_counter * 64, base_sprite=2))
                    if elem == 9:
                        print(f"Erstelle Wand an Position ({self.horizontal_segment_counter * 64}, {self.vertical_segment_counter * 64})")
            

            return self.spritegroup