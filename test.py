import pygame

try:
    img = pygame.image.load(r"db6hy2w-4db8a954-a6e1-4e46-b202-2d2786241df4 (1).png")
    print("Bild erfolgreich geladen:", img.get_size())
except pygame.error as e:
    print("Fehler beim Laden:", e)