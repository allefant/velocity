import being
import star

static LandSpriteType *type

static def tick(Being *self):
    LandSprite *sprite = LAND_SPRITE(self)
    
    if self->falling:
        being_move(self, 0, 3)
        sprite->angle += 0.2
        float h = game->middle_layer->grid->cell_h *\
            game->middle_layer->grid->y_cells
        if sprite->y >= h - 1:
            self->dead = 1

        return

    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 3) & 15

    being_move(self, 0.4 + self->flipped * 1.2, 0)

    if being_outside(self):
        self->dead = 1

    LandList *overlappers = being_collision(self)
    if overlappers:
        LandListItem *item
        for item = overlappers->first; item; item = item->next:
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                being_hit(self, collider)
                if self->falling: break


        land_list_destroy(overlappers)


def beetle_init():
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/beetle_*.png", 1, 0)), NULL)

Being * def beetle_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_BEETLE
    self->lifes = 31
    self->worth = 1000
    return self
