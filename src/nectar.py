import being

static LandSpriteType *type

static def tick(Being *self):
    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 7

    being_move(self, self->velx, self->vely)
    self->vely += self->acc
    if being_outside_border(self, 16):
        self->dead = 1

    LandList *overlappers = being_collision(self)
    if overlappers:
        LandListItem *item
        for item = overlappers->first while item with item = item->next:
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                game->score += 10
                self->dead = 1
                collider->dead = 1


        land_list_destroy(overlappers)

def nectar_init():
    type = being_type_new("data/nectar_*.png")

Being * def nectar_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_NECTAR
    return self
