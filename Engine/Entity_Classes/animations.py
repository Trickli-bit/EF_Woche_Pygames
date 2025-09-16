import Engine.entities as entities

class pick_up_animation(entities.Entity):
    def __init__(self, pos_x, pos_y, rect = entities.pygame.Rect(0,0,64,64), rect_attach = "center", scale = (64, 64), source = r"Engine\Entity_Classes\Sprites_Entity_Classes\pick_up.png", solid = False, is_spritesheet = True, fix = False, base_sprite=0, ani_frames_count=4, ani_animations={"pick_up": [0,3,5,False]}):
        super().__init__(pos_x, pos_y, rect, rect_attach, scale, source, solid, is_spritesheet, fix, base_sprite, ani_frames_count, ani_animations)

    def update(self, dx=0, dy=0, *args):
        return super().update(dx, dy, *args)
    