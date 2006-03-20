#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"
#include "star.h"

static LandSpriteType *type;

static void tick(Being *self)
{
    LandSprite *sprite = LAND_SPRITE(self);
    self->frame++;
    sprite->angle += 0.1;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 3;

    being_move(self, self->velx, self->vely);
    self->vely += 0.1;
    if (being_outside(self))
    {
        self->dead = 1;
    }
}

void star_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/star_*.png", 1, 0)), NULL);
}

Being *star_new(float x, float y)
{
    Being *self = being_new(tick, type, game->middle_layer2->grid);
    float r = land_rnd(0, AL_PI * 2);
    self->velx = sin(r) * 3 + 2;
    self->vely = cos(r) * 3;
    x += land_rnd(-1, 1);
    y += land_rnd(-1, 1);
    being_place(self, x, y);
    self->bt = BT_STAR;
    game->score++;
    return self;
}
