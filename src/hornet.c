#ifdef _PROTOTYPE_
#endif /* _PROTOTYPE_ */
#include "being.h"
#include "star.h"

static LandSpriteType *type;

static float angle;

static void evil_shot(Being *self)
{
    LandSprite *sprite = LAND_SPRITE(self);
    LandSprite *player = LAND_SPRITE(game->player);
    being_sound(self, sound->sht, 0.8, 1);
    Being *nectar = nectar_new(sprite->x - 20, sprite->y);
    float dx = player->x - sprite->x;
    float dy = player->y - sprite->y;
    float d = sqrt(dx * dx + dy * dy);
    dx /= d;
    dy /= d;
    nectar->velx = dx * 3;
    nectar->vely = dy * 3;
    LAND_SPRITE(nectar)->angle = atan2(dx, dy) + AL_PI / 2;
}

static void tick(Being *self)
{
    LandSprite *sprite = LAND_SPRITE(self);
    
    if (self->falling)
    {
        being_move(self, 0, 3);
        sprite->angle += 0.2;
        float h = game->middle_layer->grid->cell_h *
            game->middle_layer->grid->y_cells;
        if (sprite->y >= h - 1)
        {
            self->dead = 1;
            game->halt = 0;
            game->boss = 0;
        }
        return;
    }

    self->frame++;
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 3) & 15;

    if (being_outside(self))
    {
        self->dead = 1;
    }
    
    if (self->reload_ticker > 0)
        self->reload_ticker --;
        
    if (self->reload_ticker <= 0)
    {
        being_sound(self, sound->sht, 0.8, 1);
        Being *nectar1 = nectar_new(sprite->x - 20, sprite->y);
        nectar1->velx = cos(sprite->angle) * -2;
        nectar1->vely = sin(sprite->angle) * 2;
        nectar1->acc = 0.025;
        LAND_SPRITE(nectar1)->angle = sprite->angle;
        
        Being *nectar2 = nectar_new(sprite->x - 20, sprite->y);
        nectar2->velx = cos(sprite->angle) * -2;
        nectar2->vely = sin(sprite->angle) * 2 - 2;
        nectar2->acc = 0.025;
        LAND_SPRITE(nectar2)->angle = sprite->angle;
        
        self->reload_ticker = 60 - self->forward_shot * 20;
    }
    
    /*                 22,23,24,
                        /---9,19    0
                        |   ^       |
                        |   |       v
                        |   |       1--->2,12<--\
                        |   |               |   |
                        |   |   /->3,13<----/   |
                        |   |   |   |           |
                        |   |   |   \--->4,14   |
                        v   |   |           |   |        
            /-------10,20   |   |   5,15<---/   |
            |               |   |   |           |
            |               |   |   \--->6,16   |
            |               |   \-----\     |   |
            |               \-------\ |     |   |
            |                       | |     |   |
            |   /------------------>8,18    |   |
            v   |                           |   |
          11,21,7,17<-----------------------/   |
            |                                   |
            \-----------------------------------/  
     */

    float sx = game->view->scroll_x;
    float sy = game->view->scroll_y;
    switch (self->state)
    {
        case 0:
            if (game->halt)
                self->state++;
            break;
        case 1: /* move down */
        case 3:
        case 5:
        case 13:
        case 15:
            being_move(self, 0, 2);
            if (sprite->y > sy + 480 - 64)
                self->state++;
            break;
        case 2: /* move up */
        case 4:
        case 12:
        case 14:
            being_move(self, 0, -2);
            if (sprite->y < sy + 64)
            {
                self->state++;
                evil_shot(self);
            }
            break;
        case 6: /* move left */
        case 16:
            being_move(self, -2, 0);
            if (sprite->x < sx + 64)
                self->state++;
            break;
        case 7: /* move right */
        case 11:
        case 17:
        case 21:
            being_move(self, 2, 0);
            if (sprite->x > sx + 640 - 64)
            {
                evil_shot(self);
                if (self->state == 21)
                    self->state = 2;
                else
                    self->state++;
            }
            break;
        case 8: /* spawn wasp */
        case 18:
        {
            {
                Being *b = wasp_new(sprite->x, sprite->y);
            
                b->group = 9;
                game->group_active[9] = 1;
                game->group_count[9]++;
            }
            angle = 0;
            self->state++;
            break;
        }
        case 9: /* circle */
        case 19:
        case 22:
        case 23:
        case 24:
        {
            float tx = sx + 320 - sin(angle) * 180;
            float ty = sy + 240 - cos(angle) * 180;
            float dx = tx - sprite->x;
            float dy = ty - sprite->y;
            float d = sqrt(dx * dx + dy * dy);
            if (d < 5)
                angle += 0.1;
            else
            {
                dx /= d;
                dy /= d;
                if (angle > AL_PI / 4 && angle < 3 * AL_PI / 4)
                {
                    if (sprite->angle > -AL_PI / 8) sprite->angle -= 0.002;
                }
                else if (angle > 5 * AL_PI / 4 && angle < 7 * AL_PI / 4)
                {
                    if (sprite->angle < AL_PI / 8) sprite->angle += 0.002;
                }

                if (self->state == 9 || self->state == 19)
                    being_move(self, dx, dy);
                else if (self->state == 22)
                    being_move(self, dx * 2, dy * 2);
                else if (self->state == 23)
                    being_move(self, dx * 3, dy * 3);
                else if (self->state == 24)
                    being_move(self, dx * 4, dy * 4);
                
                if (angle >= AL_PI * 2)
                {
                    evil_shot(self);
                    angle = 0;
                    if (self->state == 24)
                    {
                        self->state = 10;
                        self->forward_shot = 1;
                    }
                    else
                    {
                        self->state++;
                        if (self->lifes < 111 && self->state < 22)
                        {
                            self->state = 22;
                        }
                    }
                }
            }
            break;
        }
        case 10: /* move to middle and spawn flipped wasp */
        case 20:
        {
            float dx = sx + 320 - sprite->x;
            float dy = sy + 240 - sprite->y;
            float d = sqrt(dx * dx + dy * dy);
            if (d > 1)
            {
                being_move(self, dx / d, dy / d);
            }
            else
            {
                sprite->angle = 0;
                self->state++;

                evil_shot(self);
                
                {
                    Being *b = wasp_new(sprite->x, sprite->y);
                    b->group = 9;
                    game->group_active[9] = 1;
                    game->group_count[9]++;
                    being_flip(b);
                }
            
            }
            if (sprite->angle < 0)
                sprite->angle += 0.003;
            break;
        }
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
                being_hit(self, collider);
                if (self->falling) break;
            }
        }
        land_list_destroy(overlappers);
    }
}

void hornet_init(void)
{
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/hornet_*.png", 1, 0)), NULL);
}

Being *hornet_new(float x, float y)
{
    Being *self = being_new(tick, type, game->middle_layer->grid);
    being_place(self, x, y);
    self->bt = BT_HORNET;
    self->lifes = 333;
    self->worth = 10000;
    return self;
}
