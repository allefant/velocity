import being

static LandSpriteType *type

static def tick(Being *self):
    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 7
    
    if game->halt:
        being_move(self, 0, 0.2)
    else:
        being_move(self, 0.5, 0)

    if being_outside(self):
        self->dead = 1

def honeypot_init():
    type = being_type_new("data/honeypot_*.png")

Being * def honeypot_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_HONEYPOT
    return self

LandImage * def honeypot_frame(int frame):
    return land_animation_get_frame(LAND_SPRITE_TYPE_ANIMATION(type)->animation,
        frame)
