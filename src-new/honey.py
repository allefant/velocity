import being

static LandSpriteType *type

static def tick(Being *self):
    LandSprite *sprite = LAND_SPRITE(self)
    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 8) & 3

    being_move(self, self->velx, self->vely)
    self->vely += self->acc
    if not (sprite->y < game->view->scroll_y + 1 && self->acc > 0):
        if being_outside_border(self, 32):
            self->dead = 1

def honey_init():
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/honey_*.png", 1, 0)), NULL)

Being * def honey_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    LAND_SPRITE_ANIMATED(self)->sx = -1
    being_place(self, x, y)
    self->bt = BT_HONEY
    return self
