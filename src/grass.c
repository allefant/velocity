#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"
#include "grass.h"

static LandSpriteType *type;

static void tick(Being *self)
{
    self->frame++;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 15;
}

void grass_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/grass_*.png", 1, 0)), NULL);
}

Being *grass_new(float x, float y)
{
    Being *self = being_new(tick, type, game->front_layer->grid);
    being_place(self, x, y);
    return self;
}
