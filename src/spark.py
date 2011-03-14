import being
import spark

static LandSpriteType *type

static def tick(Being *self):
    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 3

    being_move(self, self->velx, self->vely)
    self->falling++
    if self->falling > 60:
        self->dead = 1


def spark_init():
    type = being_type_new("data/spark_*.png")

Being * def spark_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer2->grid)
    float r = land_rnd(0, LAND_PI * 2)
    self->velx = sin(r) * 0.2 - 1
    self->vely = cos(r) * 0.1
    x += land_rnd(-1, 1)
    y += land_rnd(-1, 1)
    being_place(self, x, y)
    self->bt = BT_SPARK
    return self
