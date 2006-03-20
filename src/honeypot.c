#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"

static LandSpriteType *type;

static void tick(Being *self)
{
    self->frame++;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 7;
    
    if (game->halt)
        being_move(self, 0, 0.2);
    else
        being_move(self, 0.5, 0);

    if (being_outside(self))
    {
        self->dead = 1;
    }

}

void honeypot_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/honeypot_*.png", 1, 0)), NULL);
}

Being *honeypot_new(float x, float y)
{
    Being *self = being_new(tick, type, game->middle_layer->grid);
    being_place(self, x, y);
    self->bt = BT_HONEYPOT;
    return self;
}

LandImage *honeypot_frame(int frame)
{
    return land_animation_get_frame(LAND_SPRITE_TYPE_ANIMATION(type)->animation,
        frame);
}
