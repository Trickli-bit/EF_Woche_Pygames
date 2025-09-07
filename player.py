def calculating_movement(self, keys):
    dx = dy = 0
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= self.speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += self.speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= self.speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += self.speed

    # Diagonalbewegung anpassen (optional, für gleichmäßige Geschwindigkeit)
    if dx != 0 and dy != 0:
        dx = int(dx / 1.4142)
        dy = int(dy / 1.4142)

    self.rect.x += dx
    self.rect.y += dy


    
        self.rect.x += self.dx
        self.rect.y += self.dy