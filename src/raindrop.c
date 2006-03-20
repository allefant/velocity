#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"

static LandSpriteType *type;

static void tick(Being *self)
{
    if (self->falling)
    {
        self->dead = 1;
        return;
    }

    self->frame++;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 4) & 3;

    self->vely += self->acc;
    being_move(self, self->velx, self->vely);

    if (being_outside(self))
    {
        self->dead = 1;
    }
    
    LandList *overlappers = being_collision(self);
    if (overlappers)
    {
        LandListItem *item;
        for (item = overlappers->first; item; item = item->next)
        {
            Being *collider = item->data;
            if (collider->bt == BT_HONEY)
            {
                being_hit(self, collider);
                if (self->falling) break;
            }
        }
        land_list_destroy(overlappers);
    }

}

void raindrop_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/raindrop_*.png", 1, 0)), NULL);
}

Being *raindrop_new(float x, float y)
{
    Being *self = being_new(tick, type, game->middle_layer->grid);
    being_place(self, x, y);
    self->bt = BT_RAINDROP;
    self->vely = 1;
    self->velx = 0.5;
    self->acc = 0.04;
    self->worth = 50;
    return self;
}
