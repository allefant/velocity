import being

static LandSpriteType *type

static def tick(Being *self):
    if self->falling:
        self->dead = 1
        return

    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 4) & 3

    self->vely += self->acc
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

def raindrop_init():
    type = being_type_new("data/raindrop_*.png")

Being * def raindrop_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_RAINDROP
    self->vely = 1
    self->velx = 0.5
    self->acc = 0.04
    self->worth = 50
    return self
