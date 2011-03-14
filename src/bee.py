import being
import honey

static LandSpriteType *type
static void(*orig_draw)(LandSprite *self, LandView *view)
static LandAnimation *shield_anim

static def tick(Being *self):
    LandSprite *sprite = LAND_SPRITE(self)

    if self->falling:
        being_move(self, 0, 3)
        sprite->angle += 0.2
        if being_outside(self):
            being_sound(self, sound->gov, 1, 1)
            self->dead = 1

        return

    self->velx += game->kx * 0.2
    self->vely += game->ky * 0.2
    self->velx *= 0.97
    self->vely *= 0.97
    
    if game->wind:
        if game->frame % (int)game->FPS < 20:
            float a = LAND_PI * game->frame / (game->FPS * 2)
            self->velx += 0.15 * cos(a) - 0.08
            self->vely += 0.15 * sin(a) + 0.08


    if self->reload_ticker > 0:
        self->reload_ticker -= 1

    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 4) & 15

    if game->kf:
        if self->reload_ticker == 0 or self->reload_ticker == 15 or\
            self->reload_ticker == 30 or self->reload_ticker == 45:
            int extra = self->reload_ticker == 15 ? 1 :\
                self->reload_ticker == 45 ? 2 : 0
            if self->forward_shot > extra:
                being_sound(self, sound->sho, 0.5, 1)
                Being *honey = honey_new(sprite->x + 20, sprite->y + 10)
                honey->velx = 6

            if self->back_shot > extra:
                being_sound(self, sound->sho, 0.4, 0.84)
                Being *honey2 = honey_new(sprite->x - 20, sprite->y)
                honey2->velx = 0
                honey2->vely = -4
                honey2->acc = 0.1

            if self->down_shot > extra:
                being_sound(self, sound->sho, 0.25, 1.5)
                if self->cannon1:
                    Being *honey2 = honey_new(sprite->x + 20, sprite->y + 10)
                    honey2->velx = 1
                    honey2->vely = 4

                else:
                    Being *honey3 = honey_new(sprite->x + 20, sprite->y + 10)
                    honey3->velx = 1
                    honey3->vely = -4

                self->cannon1 ^= 1

            if self->triple_shot > extra:
                being_sound(self, sound->sho, 0.3, 1.26)
                if self->cannon2:
                    Being *honey2 = honey_new(sprite->x + 20, sprite->y + 10)
                    honey2->velx = 6
                    honey2->vely = 2

                else:
                    Being *honey3 = honey_new(sprite->x + 20, sprite->y + 10)
                    honey3->velx = 6
                    honey3->vely = -2

                self->cannon2 ^= 1

            if self->reload_ticker == 0:
                self->reload_ticker = 60


    float dx = self->velx
    float dy = self->vely
    float d = sqrt(dx * dx + dy * dy)
    if d > 3:
        dx = 3 * dx / d
        dy = 3 * dy / d

    # Auto-fly 1 pixel / tick. 
    if not game->halt: dx += 1

    being_move(self, dx, dy)
    
    # Ensure we never move outside the visible screen. 
    float b = 24
    if sprite->x < game->view->scroll_x + b:
        being_move(self, game->view->scroll_x + b - sprite->x, 0)
    if sprite->x > game->view->scroll_x + game->view->w - b:
        being_move(self, game->view->scroll_x + game->view->w - b - sprite->x, 0)
    if sprite->y < game->view->scroll_y + b:
        being_move(self, 0, game->view->scroll_y + b - sprite->y)
    if sprite->y > game->view->scroll_y + game->view->h - b:
        being_move(self, 0, game->view->scroll_y + game->view->h - b - sprite->y)

    if sprite->y > 640:
        if game->water:
            if self->frame % 5 == 0:
                spark_new(sprite->x, sprite->y + 20)
                self->velx -= 0.3
                self->vely *= 0.5


        elif  sprite->y > 704:
            being_move(self, 0, 704 - sprite->y)

    if self->invisible:
        self->invisible--

    LandList *overlappers = being_collision(self)
    if overlappers:
        int solid = 0
        LandListItem *item
        for item = overlappers->first while item with item = item->next:
            int got_hit = 0
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                continue
            if collider->bt == BT_DROP:
                got_hit = 1
                collider->dead = 1

            elif  collider->bt == BT_NECTAR:
                got_hit = 1
                collider->dead = 1

            elif  collider->bt == BT_BLOOD:
                got_hit = 1
                collider->dead = 1

            elif  collider->bt == BT_FLY: got_hit = 2
            elif  collider->bt == BT_MOSQUITO: got_hit = 2
            elif  collider->bt == BT_WASP: got_hit = 2
            elif  collider->bt == BT_FLEA: got_hit = 2
            elif  collider->bt == BT_STRIDER: got_hit = 2
            elif  collider->bt == BT_BEETLE: got_hit = 2
            elif  collider->bt == BT_RAINDROP: got_hit = 2
            elif  collider->bt == BT_HORNET: got_hit = 2
            elif  collider->bt == BT_HONEYPOT:
                being_sound(self, sound->tat, 1, 1)
                collider->dead = 1
                self->pots++
                game->score += 150
                if self->pots == 3:
                    if self->back_shot == 0:
                        self->back_shot = 1
                    elif  self->triple_shot == 0:
                        self->triple_shot = 1
                    elif  self->down_shot == 0:
                        self->down_shot = 1
                    elif  self->forward_shot == 1:
                        self->forward_shot = 2
                    elif  self->back_shot == 1:
                        self->back_shot = 2
                    elif  self->triple_shot == 1:
                        self->triple_shot = 2
                    elif  self->down_shot == 1:
                        self->down_shot = 2
                    elif  self->forward_shot == 2:
                        self->forward_shot = 3
                    elif  self->back_shot == 2:
                        self->back_shot = 3
                    elif  self->triple_shot == 2:
                        self->triple_shot = 3
                    elif  self->down_shot == 2:
                        self->down_shot = 3
                    elif  self->shield == 0:
                        self->shield = 1
                    else: # Already got all powerups -> get score instead.
                        int wave = 1 + game->last_pos / 6400
                        game->score += wave * 1000

                    self->pots = 0

                continue

            if self->invisible: continue

            if got_hit == 2:
                if collider->falling:
                    got_hit = 0
                else:
                    being_hit(collider, NULL)


            if got_hit:
                if self->shield:
                    self->shield--
                elif  self->lifes > 0:
                    being_sound(self, sound->aye, 1, 1)
                    self->lifes--
                    self->invisible = game->FPS * 3

                else:
                    being_sound(self, sound->aye, 1, 1)
                    self->falling = 1


            solid = 1

        land_list_destroy(overlappers)
        
        if solid:
            being_move(self, -dx, -dy)
            self->velx -= dx * 2
            self->vely -= dy * 2



static def draw(LandSprite *self, LandView *view):
    float x = self->x - view->scroll_x + view->x
    float y = self->y - view->scroll_y + view->y
    Being *being = BEING(self)
    if ((being->invisible >> 3) & 1) == 0:
        orig_draw(self, view)

    if being->shield:
        land_image_draw_rotated(land_animation_get_frame(shield_anim,
            (being->frame / 8) & 7), x, y,
            being->frame * LAND_PI / 100)


def bee_init():
    type = being_type_new("data/bee_*.png");
    shield_anim = land_animation_new(land_load_images("data/shield_*", 1, 0))
    orig_draw = type->draw
    type->draw = draw

Being * def bee_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    LAND_SPRITE_ANIMATED(self)->sx = -1
    being_place(self, x, y)
    self->bt = BT_BEE
    self->forward_shot = 1
    self->lifes = 2
    return self
