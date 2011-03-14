import being

static LandSpriteType *type

static def tick(Being *self):
    LandSprite *sprite = LAND_SPRITE(self)
    if self->falling:
        being_move(self, 0, 3)
        sprite->angle += 0.05
        float h = game->middle_layer->grid->cell_h *\
            game->middle_layer->grid->y_cells
        if sprite->y >= h - 1:
            self->dead = 1

        return

    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 10) & 7

    self->vely += self->acc
    self->acc = 0.03 * sin(LAND_PI * self->frame / (float)game->FPS)
    being_move(self, self->velx, self->vely)

    if being_outside(self):
        self->dead = 1

    LandList *overlappers = being_collision(self)
    if overlappers:
        LandListItem *item
        for item = overlappers->first while item with item = item->next:
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                being_hit(self, collider)
                if self->falling: break


        land_list_destroy(overlappers)

def leaf_init():
    type = being_type_new("data/leaf_*.png")

Being * def leaf_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_LEAF
    self->worth = 300
    self->lifes = 11
    return self
