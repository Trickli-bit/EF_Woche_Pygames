import pygame
import generation

Map = generation.generateLandscape("Main/mapCSV.csv")
Map.generate_map()
