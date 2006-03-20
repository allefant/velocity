#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"

static LandSpriteType *type;

static void tick(Being *self)
{
    self->frame++;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 7;

    being_move(self, self->velx, self->vely);
    self->vely += self->acc;
    if (being_outside_border(self, 16))
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
                game->score += 10;
                self->dead = 1;
                collider->dead = 1;
            }
        }
        land_list_destroy(overlappers);
    }

}

void nectar_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/nectar_*.png", 1, 0)), NULL);
}

Being *nectar_new(float x, float y)
{
    Being *self = being_new(tick, type, game->middle_layer->grid);
    being_place(self, x, y);
    self->bt = BT_NECTAR;
    return self;
}
