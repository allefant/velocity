macro BEING(_) ((Being *)(_))

import game
import honeypot

enum BeingType:
    BT_BEE
    BT_FLY
    BT_HONEY
    BT_STAR
    BT_STRIDER
    BT_DROP
    BT_SPARK
    BT_WASP
    BT_NECTAR
    BT_MOSQUITO
    BT_BLOOD
    BT_HONEYPOT
    BT_BEETLE
    BT_FLEA
    BT_RAINDROP
    BT_LEAF
    BT_HORNET

class Being:
    LandSpriteAnimated super
    
    LandGrid *grid
    
    int bt # type, see enum above 
    int frame
    float velx, vely
    float acc
    float reload_ticker
    
    int lifes
    int worth
    
    unsigned int pots with 2
    
    unsigned int forward_shot with 2
    unsigned int down_shot with 2
    unsigned int triple_shot with 2
    unsigned int back_shot with 2
    unsigned int shield with 2

    int state
    unsigned int falling with 1
    unsigned int dead with 1
    unsigned int flipped with 1
    unsigned int cannon1 with 1
    unsigned int cannon2 with 1

    int group
    int spawn_time
    int invisible

    void (*tick)(Being *self)

import being

Being * def being_new(void (*tick)(Being *),
    LandSpriteType *type, LandGrid *grid):
    Being *self
    land_alloc(self)
    land_sprite_animated_initialize(LAND_SPRITE(self), type)
    self->tick = tick
    self->grid = grid
    self->lifes = 1
    self->spawn_time = game->frame
    land_add_list_data(&game->beings, self)
    return self

def being_sound(Being *self, LandSound *sample, float vol, float frequency):
    float d = LAND_SPRITE(self)->x - LAND_SPRITE(game->player)->x
    float pan = d / 128.0
    if pan < -1: pan = -1
    if pan > 1: pan = 1
    d = 255 + 50 - fabs(d) / 5
    float v = d / 255.0
    if v <= 0: return
    if v > 1: v = 1
    land_sound_play(sample, v, pan, frequency)
    # if voice >= 0:
    #    int p = 128
    #    if sample == sound->sho: p = 0
    #    if sample == sound->hit: p = 1
    #    if sample == sound->sht || sample == sound->cin: p = 64
    #    if sample == sound->tat: p = 192
    #    if sample == sound->aye || sample == sound->gov: p = 255
    #    voice_set_priority(voice, p)


def being_place(Being *self, float x, float y):
    land_sprite_place_into_grid(LAND_SPRITE(self), self->grid, x, y)

def being_shot_down(Being *self):
    game->kills++
    being_sound(self, sound->bom, 1, 1)
    if self->group:
        game->group_hit[self->group]++
        if game->group_active[self->group]:
            if game->group_hit[self->group] == game->group_count[self->group]:
                honeypot_new(LAND_SPRITE(self)->x, LAND_SPRITE(self)->y)




def being_hit(Being *self, Being *collider):
    being_sound(self, sound->hit, 0.5, 1)
    self->lifes--
    if game->easy:
        self->lifes--
    if collider:
        collider->dead = 1
        star_new(LAND_SPRITE(collider)->x, LAND_SPRITE(collider)->y)

    if self->lifes <= 0:
        if self->flipped:
            game->score += self->worth * 2
        else:
            game->score += self->worth
        being_shot_down(self)
        self->falling = 1
        if collider:
            int i
            for i = 0 while i < 8 with i++:
                star_new(LAND_SPRITE(collider)->x, LAND_SPRITE(collider)->y)



def being_destroy(Being *self):
    # If a bonus object gets destroyed, it either went out of view, or was
    # shot down. In the latter case, it counts towards group bonuses, in
    # the former, the group bonus is lost.
    #
    if self->group:
        game->group_out[self->group]++
        if game->group_active[self->group]:
            if game->group_out[self->group] == game->group_count[self->group]:
                game->group_active[self->group] = 0
                game->group_count[self->group] = 0
                game->group_hit[self->group] = 0
                game->group_out[self->group] = 0

    land_sprite_remove_from_grid(LAND_SPRITE(self),
        self->grid)
    land_sprite_destroy(LAND_SPRITE(self))

def being_move(Being *self, float dx, float dy):
    land_sprite_move(LAND_SPRITE(self), self->grid, dx, dy)

LandList * def being_collision(Being *self):
    return land_sprites_grid_overlap(LAND_SPRITE(self), self->grid)

int def being_outside_border(Being *self, int border):
    float l = -border, t = -border, r = border, b = border
    LandSprite *sprite = LAND_SPRITE(self)
    float w = self->grid->cell_w * self->grid->x_cells
    float h = self->grid->cell_h * self->grid->y_cells
    if sprite->x <= 1 or sprite->y <= 1 or sprite->x >= w - 1 or\
        sprite->y >= h - 1:
        return 1

    l += game->view->scroll_x + game->view->x
    t += game->view->scroll_y + game->view->y
    r += game->view->scroll_x + game->view->x + game->view->w
    b += game->view->scroll_y + game->view->y + game->view->h
    if sprite->x < l || sprite->y < t || sprite->x > r || sprite->y > b:
        return 1
    return 0

int def being_outside(Being *self):
    # Give freshly spawned ones one second to appear. 
    if game->frame - self->spawn_time < game->FPS: return 0
    return being_outside_border(self, 32)

def being_flip(Being *self):
    self->flipped = !self->flipped
    LAND_SPRITE_ANIMATED(self)->sx = (self->flipped * -2) + 1

LandSpriteType *def being_type_new(char const *pattern):
    return land_spritetype_animation_new(
        land_animation_new(
            land_load_images(pattern, True, 0)), None, True, 1)
