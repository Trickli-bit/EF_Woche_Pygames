
import Engine.entities as entites
import Main.settings as settings

class Turtle(entites.EntityMovable):
    def __init__(self, pos_x, pos_y, rect=(0, 0, 64, 64), rect_attach="topleft",
                 scale=(128, 128),
                 source=r"Engine\Entity_Classes\Sprites_Entity_Classes\Turtle.png",
                 solid=False, is_spritesheet=True, fix=False, base_sprite=0,
                 ani_frames_count=20,
                 ani_animations={"walking_a": [0, 1, 5, True], "walking_d": [3, 4, 5, True],
                                 "walking_s": [6, 7, 5, True], "walking_w": [9, 10, 5, True],
                                 "burning_s": [12, 13, 5, False], "burning_d": [14, 15, 5, False],
                                 "burning_a": [16,17, 5, False], "burning_w": [18, 19, 5, False]},  width_blocks = 0, height_blocks = 0):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)
        
        # Rechteck-Seiten in Pixeln (Vielfache von 64)
        self.width = width_blocks * 64
        self.height = height_blocks * 64

        # Startposition merken
        self.start_x = pos_x
        self.start_y = pos_y


        # Bewegungsrichtung
        self.direction = "right"
        self.speed = 2
        self.dead = False
        self.dead_counter = 0

    def movement(self):
        dx, dy = 0, 0

        if self.direction == "right":
            dx = self.speed
            if self.rect.x + dx >= self.start_x + self.width:
                self.direction = "down"

        elif self.direction == "down":
            dy = self.speed
            if self.rect.y + dy >= self.start_y + self.height:
                self.direction = "left"

        elif self.direction == "left":
            dx = -self.speed
            if self.rect.x + dx <= self.start_x:
                self.direction = "up"

        elif self.direction == "up":
            dy = -self.speed
            if self.rect.y + dy <= self.start_y:
                self.direction = "right"
        
        return dx, dy
    
    def die(self):
        self.dead_counter += 1
        self.dead = True
        print(self.dead_counter)
        if self.direction == "right":
            self.Animation.start_animation("burning_d")
        if self.direction == "left":
            self.Animation.start_animation("burning_a")
        if self.direction == "up":
            self.Animation.start_animation("burning_w")
        if self.direction == "down":
            self.Animation.start_animation("burning_s")
        if self.dead_counter == 120:
            self.kill()

    def update(self, dx=0, dy=0, *args):
        if not self.dead:
            dtx, dty = self.movement()
        else:
            dtx, dty = 0, 0
            self.direction == ""
            self.die()
        print(dx,dy, self.start_x, self.start_y)
        self.start_x += dx
        self.start_y += dy
        self.dx = dtx
        self.dy = dty
        super().update(dx + dtx, dy + dty, *args)

        


        
        