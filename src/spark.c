#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"
#include "spark.h"

static LandSpriteType *type;

static void tick(Being *self)
{
    self->frame++;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 3;

    being_move(self, self->velx, self->vely);
    self->falling++;
    if (self->falling > 60)
    {
        self->dead = 1;
    }
}

void spark_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/spark_*.png", 1, 0)), NULL);
}

Being *spark_new(float x, float y)
{
    Being *self = being_new(tick, type, game->middle_layer2->grid);
    float r = land_rnd(0, AL_PI * 2);
    self->velx = sin(r) * 0.2 - 1;
    self->vely = cos(r) * 0.1;
    x += land_rnd(-1, 1);
    y += land_rnd(-1, 1);
    being_place(self, x, y);
    self->bt = BT_SPARK;
    return self;
}
