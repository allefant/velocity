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

    if being_outside(self):
        self->dead = 1

    if self->reload_ticker > 0:
        self->reload_ticker --
        
    if self->reload_ticker <= 0:
        Being *nectar1 = nectar_new(sprite->x - 20, sprite->y)
        nectar1->velx = -2 + self->flipped * 5
        nectar1->vely = -2
        nectar1->acc = 0.025

        being_sound(self, sound->sht, 0.8, 1)

        self->reload_ticker = 100

    if sprite->y > LAND_SPRITE(game->player)->y + 1:
        being_move(self, 0, -0.25)
        
    if sprite->y < LAND_SPRITE(game->player)->y - 1:
        being_move(self, 0, 0.25)
    
    if game->halt:
        float tx = game->view->scroll_x +\
            (self->flipped ? 64 : 640 - 64)
        if sprite->x < tx - 2:
            being_move(self, 1, 0)
        elif  sprite->x > tx + 2:
            being_move(self, -1, 0)

    else:
        being_move(self, self->flipped * 2.5, 0)

    LandList *overlappers = being_collision(self)
    if overlappers:
        LandListItem *item
        for item = overlappers->first while item with item = item->next:
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                being_hit(self, collider)
                if self->falling: break

            if collider->bt == BT_WASP:
                float dx = LAND_SPRITE(collider)->x - sprite->x
                float dy = LAND_SPRITE(collider)->y - sprite->y
                float d = sqrt(dx * dx + dy * dy)
                dx /= d
                dy /= d
                if dy < 0 && sprite->y < game->view->scroll_y + 240:
                    dy = 0
                if dy > 0 && sprite->y > game->view->scroll_y + 240:
                    dy = 0
                being_move(self, -dx * 2, - dy * 2)
                being_move(collider, dx * 2, dy * 2)


        land_list_destroy(overlappers)


def wasp_init():
    type = being_type_new("data/wasp_*.png")

Being * def wasp_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_WASP
    self->lifes = 6
    self->worth = 400
    self->reload_ticker = 70
    return self
