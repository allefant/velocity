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

    if self->state == 2:
        LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 3) & 15
        self->frame++
        if self->frame == 3 * 16:
            self->frame = 0
            self->state++

        being_move(self, self->flipped * 4, self->vely)

    if self->state == 0:
        LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 3) & 15
        self->frame++
        if self->frame == 3 * 8:
            self->state++


    elif  self->state == 3:
        self->vely += 0.1
        being_move(self, self->flipped * 4, self->vely)

        if sprite->y > 11 * 64:
            self->state = 0
            self->vely = -9
            being_sound(self, sound->boi, 1, 1)


    elif  self->state == 1:
        self->vely += 0.11
        being_move(self, self->flipped * 4, self->vely)
        
        if self->vely >= 0:
            self->state = 2


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


def flea_init():
    type = being_type_new("data/flea_*.png")

Being * def flea_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_FLEA
    self->lifes = 4
    self->state = 3
    self->worth = 300
    return self
