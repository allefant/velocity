import being
import star
import blood

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
    
    if self->flipped:
        being_move(self, 2, 0)

    if self->state:
        switch (self->state):
            case 1:
                if sprite->x <= game->view->scroll_x + game->view->w - 32:
                    self->state++
                break
            case -1:
                if sprite->x <= game->view->scroll_x + game->view->w - 32:
                    self->state--
                break
            case 2:
                being_move(self, 1, -1)
                if sprite->y <= game->view->scroll_y + 32: self->state++
                break
            case -2:
                being_move(self, 1, 1)
                if sprite->y >= game->view->scroll_y + game->view->h - 32:
                    self->state--
                break
            case 3:
                if sprite->x <= game->view->scroll_x + 32: self->state++
                break
            case -3:
                if sprite->x <= game->view->scroll_x + 32: self->state--
                break
            case 4:
                being_move(self, 1, 1)
                if sprite->y >= game->view->scroll_y + game->view->h - 32:
                    self->state++
                break
            case -4:
                being_move(self, 1, -1)
                if sprite->y <= game->view->scroll_y + 32:
                    self->state--
                break
            case 5:
            case -5:
                being_move(self, 3, 0)
                LAND_SPRITE_ANIMATED(self)->sx = -1
                break


    if self->frame > 100 and being_outside(self):
        self->dead = 1

    if self->reload_ticker > 0:
        self->reload_ticker --
        
    # Don't shoot at very screen edge. 
    if self->reload_ticker <= 0 and sprite->x > game->view->scroll_x + 32:
        being_sound(self, sound->cin, 0.8, 1)
        float dx = LAND_SPRITE(game->player)->x - sprite->x
        float dy = LAND_SPRITE(game->player)->y - sprite->y
        float d = sqrt(dx * dx + dy * dy)
        Being *blood = blood_new(sprite->x, sprite->y)
        blood->velx = dx / d + 1
        blood->vely = dy / d

        self->reload_ticker = 300

    LandList *overlappers = being_collision(self)
    if overlappers:
        LandListItem *item
        for item = overlappers->first while item with item = item->next:
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                being_hit(self, collider)
                if self->falling: break


        land_list_destroy(overlappers)


def mosquito_init():
    type = being_type_new("data/mosquito_*.png")

Being * def mosquito_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_MOSQUITO
    self->reload_ticker = 360
    self->lifes = 5
    self->worth = 250
    return self
