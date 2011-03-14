import being
import grass

static LandSpriteType *type

static def tick(Being *self):
    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 15

def grass_init():
    type = being_type_new("data/grass_*.png")

Being * def grass_new(float x, float y):
    Being *self = being_new(tick, type, game->front_layer->grid)
    being_place(self, x, y)
    return self
