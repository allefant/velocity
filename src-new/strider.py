import being
import drop
import spark
import strider

static LandSpriteType *type

static def tick(Being *self):
    LandSprite *sprite = LAND_SPRITE(self)
    
    if self->falling:
        being_move(self, 0, 2)
        sprite->angle += 0.05
        float h = game->middle_layer->grid->cell_h *\
            game->middle_layer->grid->y_cells
        if sprite->y >= h - 1:
            self->dead = 1

        return

    if self->frame % 25 == 0:
        float dx[] = {18, 34 , 115, 100}
        float dy[] = {77, 102, 88 , 66}
        int foot = land_rand(0, 3)
        spark_new(sprite->x - 64 + dx[foot], sprite->y - 64 + dy[foot])

    if self->reload_ticker > 0:
        self->reload_ticker --

    self->frame++
    LAND_SPRITE_ANIMATED(self)->frame = (self->frame / 3) & 15

    being_move(self, -1 + self->flipped * 3, 0)

    if being_outside(self):
        self->dead = 1

    #  
       #dx/dy -> vector to player
       #vx/vy -> player velocity
       #u/v -> projectile velocity
       #s -> projectile speed
       #t -> ticks until hit

        #we hit when:
       #dx + vx * t = u * t (1)
       #dy + vy * t = v * t (2)
       
        #constrained by speed of projectile:
       #u * u + v * v = s * s (3)
       
        #solve for u/v/t:
       #(1) u = dx / t + vx (4)
       #(2) v = dy / t + vy (5)
       #(4+5 in 3) (dx * dx + dy * dy) / (t * t) +
           #2 * (dx * vx + dy * vy) / t +
           #vx * vx + vy * vy - s * s = 0

        #A = dx * dx + dy * dy
       #B = 2 * (dx * vx + dy * vy)
       #C = vx * vx + vy * vy - s * s

        #D = B * B - 4 * A * C

        #1/t1 = (sqrt(D) - B) / (2 * A)
       #1/t2 = (-sqrt(D) - B) / (2 * A)
		
    #
    
    float dx = LAND_SPRITE(game->player)->x - (sprite->x - 30)
    float dy = LAND_SPRITE(game->player)->y - (sprite->y - 10)
    if (dx < 0 && !self->flipped) || (dx > 0 && self->flipped):
        if self->reload_ticker <= 0:
            self->reload_ticker = 20
            float vx = 1
            float vy = 0
            float s = 3
            float A = dx * dx + dy * dy
            float B = 2 * (dx * vx + dy * vy)
            float C = vx * vx + vy * vy - s * s
            float D = B * B - 4 * A * C
            
            if D >= 0:
                float s1 = (sqrt(D) - B) / (2 * A)
                float s2 = (-sqrt(D) - B) / (2 * A)
                if s1 > 0 || s2 > 0:
                    being_sound(self, sound->blu, 1, 1)
                    float t_ = s1
                    if t_ < s2: t_ = s2 # Take solution in future. 
                    
                    Being *drop = drop_new(sprite->x - 30, sprite->y - 10)
                    drop->velx = dx * t_ + vx
                    drop->vely = dy * t_ + vy
                    LAND_SPRITE(drop)->angle =\
                        atan2(drop->velx, drop->vely) + AL_PI / 2
                    self->reload_ticker += 60




    LandList *overlappers = being_collision(self)
    if overlappers:
        LandListItem *item
        for item = overlappers->first; item; item = item->next:
            Being *collider = item->data
            if collider->bt == BT_HONEY:
                being_hit(self, collider)
                if self->falling: break


        land_list_destroy(overlappers)


def strider_init():
    type = land_spritetype_animation_new(
        land_animation_new(
        land_load_images("data/strider_*.png", 1, 0)), NULL)

Being * def strider_new(float x, float y):
    Being *self = being_new(tick, type, game->middle_layer->grid)
    being_place(self, x, y)
    self->bt = BT_STRIDER
    self->lifes = 5
    self->worth = 500
    return self
