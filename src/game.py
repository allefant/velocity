import global land.land
import being
import menu

import bee
import fly
import honey
import grass
import star
import strider
import drop
import spark
import wasp
import nectar
import mosquito
import blood
import beetle
import flea
import raindrop
import leaf
import hornet

import levels

class Game:
    LandMap *map

    LandLayer *back_layer
    LandLayer *back_layer2
    LandLayer *back_layer3
    LandLayer *middle_layer
    LandLayer *middle_layer2
    LandLayer *front_layer

    LandView *view

    int group_count[10]
    int group_out[10]
    int group_hit[10]
    int group_active[10]
    
    int next_life_score

    LandList *beings
    Being *player

    int easy
    int score
    int kills
    int game_over
    int won
    int start_wave
    int checkpoint
    
    float kx, ky, kf
    
    float last_pos
    float target_scroll_y
    int water
    int wind
    int halt
    int boss

    int frame

    double fps, fps_accumulator, fps_time
    double FPS
    
    int playback_active, playback_pos, playback_allocated
    char *playback
    
    int recording_active, recording_pos, recording_allocated
    char *recording

class Sound:
    LandSound *sho,\ # player bullet, p0 
        *blu,\ # strider bullet, p128 
        *bom,\ # enemy down, p128 
        *aye,\ # player hit, p255 
        *hit,\ # enemy is hit, p1 
        *gov,\ # player down, p255 
        *tat,\ # power up, p192 
        *sht,\ # wasp/hornet bullet, p64 
        *cin,\ # mosquito bullet, p64 
        *boi # flea jump, p128 

static import game

static LandArray *backgrass[8]
static LandArray *backdrop
static LandArray *backdrop2
static LandImage *backearth

global Sound *sound
global Game *game
static char const *message = NULL
static int message_time = 0

static int waves_count = 12
static int wave_length = 100

static LandImage *capture_frame

class MEMFILE:
    unsigned char *mem
    int pos
    int size

static macro M MEMFILE *m = (void *)userdata

#static int def pf_fclose(void *userdata):
#    return 0;

#static int def pf_getc(void *userdata):
#    M
#    if m->pos < m->size:
#        return m->mem[m->pos++]
#    return EOF

#static int def pf_ungetc(int c, void *userdata):
#    return c

#static long def pf_fread(void *p, long n, void *userdata):
#    M
#    n = min(n, m->size - m->pos)
#    if n > 0:
#        memcpy(p, m->mem + m->pos, n)
#        m->pos += n

#    else:
#        n = 0
#    return n

#static int def pf_putc(int c, void *userdata):
#    return 0
#static long def pf_fwrite(const void *p, long n, void *userdata):
#    return 0
#static int def pf_fseek(void *userdata, int offset): M; m->pos += offset:
#    return 0
#static int def pf_feof(void *userdata):
#    M
#    return m->pos >= m->size
#static int def pf_ferror(void *userdata):
#    return 0;

#static PACKFILE_VTABLE vtable = {
#    pf_fclose, pf_getc, pf_ungetc, pf_fread, pf_putc, pf_fwrite, pf_fseek,
#    pf_feof, pf_ferror}

static LandSound *def sample(char const *name):
    #MEMFILE mem
    #land_log_message("land_sound_load %s..", name)
    #mem.mem = land_datafile_read_entry(land_get_datafile(), name, &mem.size)
    #mem.pos = 0
    LandSound *sam = None
    #PACKFILE *pf = pack_fopen_vtable(&vtable, &mem)
    #sam = load_wav_pf(pf)
    # if not sam:
    #    sam = load_sample(name)

    # else:
    #    land_log_message_nostamp(" [memory %d] ", mem.size)
    #land_log_message_nostamp(sam ? "success.\n" : "failure.\n")
    sam = land_sound_load(name)
    return sam

static def load():
    int i
    static int once = 0
    if once: return
    once++
    
    land_alloc(sound)
    sound->sho = sample("data/sound/sho.ogg")
    sound->blu = sample("data/sound/blu.ogg")
    sound->bom = sample("data/sound/bom.ogg")
    sound->aye = sample("data/sound/aye.ogg")
    sound->hit = sample("data/sound/hit.ogg")
    sound->gov = sample("data/sound/gov.ogg")
    sound->tat = sample("data/sound/tat.ogg")
    sound->sht = sample("data/sound/sht.ogg")
    sound->cin = sample("data/sound/cin.ogg")
    sound->boi = sample("data/sound/boi.ogg")

    backdrop = land_image_load_split_sheet("data/background.jpg",
        0, 0, 512, 512, 0, 0, 8, 1, 0)
    for i = 0 while i < 8 with i++:
        char name[256]
        snprintf(name, sizeof name, "data/backgrass_%02d.png", 1 + i)
        backgrass[i] = land_image_load_split_sheet(name,
            0, 0, 256, 256, 0, 0, 8, 1, 0)

    backdrop2 = land_load_images("data/backwater_*.png", 0, 0)

    backearth = land_image_load("data/backearth.png")

    bee_init()
    fly_init()
    honey_init()
    grass_init()
    star_init()
    strider_init()
    drop_init()
    spark_init()
    wasp_init()
    nectar_init()
    mosquito_init()
    blood_init()
    honeypot_init()
    beetle_init()
    flea_init()
    raindrop_init()
    leaf_init()
    hornet_init()

def game_begin(int wave, int easy):
    int w = 64 * wave_length * waves_count
    int h = 64 * 12

    if game:
        # Garbage collection - yes, 2 lines I could have saved with automatic
        # GC (in the whole code of the game :P)
        #
        if game->map: land_map_del(game->map)
        if game->beings: land_list_destroy(game->beings)
        land_free(game)

    land_alloc(game)
    
    game->easy = easy

    game->FPS = 100

    game->map = land_map_new()

    # sky 
    game->back_layer = land_layer_new_with_grid(
        land_tilegrid_new(512, 512, w / 512, 1))
    # grass 
    game->back_layer2 = land_layer_new_with_grid(
        land_tilegrid_new(256, 256, w / 256, 1))
    # water 
    game->back_layer3 = land_layer_new_with_grid(
        land_tilegrid_new(1024, 128, w / 1024, 1))

    # sprites 
    game->middle_layer = land_layer_new_with_grid(
        land_sprites_grid_new(64, 64, w / 64, h / 64))
    # foreground particles 
    game->middle_layer2 = land_layer_new_with_grid(
        land_sprites_grid_new(64, 64, w / 64, h / 64))

    # foreground background 
    game->front_layer = land_layer_new_with_grid(
        land_sprites_grid_new(64, 64, w / 64, h / 64))

    land_map_add_layer(game->map, game->back_layer)
    land_map_add_layer(game->map, game->back_layer2)
    land_map_add_layer(game->map, game->back_layer3)
    land_map_add_layer(game->map, game->middle_layer)
    land_map_add_layer(game->map, game->middle_layer2)
    land_map_add_layer(game->map, game->front_layer)

    game->view = land_view_new(0, 0, land_display_width(),
        land_display_height())

    int i
    for i = 0 while i < wave_length * waves_count * 64 with i += land_rand(64, 512):
        grass_new(i, h - 80)

    land_layer_set_scroll_speed(game->front_layer, 1.4, 1)
    
    float f = (512 - 480.0) / (h - 480.0)
    land_layer_set_scroll_speed(game->back_layer, f, f)
    for i = 0 while i < game->back_layer->grid->x_cells with i++:
        land_tilegrid_place(game->back_layer->grid, i, 0,
            land_array_get_nth(backdrop, (i + 7) & 7))

    land_layer_set_position(game->back_layer3, 0, 480 * 2 + 32)
    land_layer_set_scroll_speed(game->back_layer3, 1, 0.5)

    f = 0.5
    land_layer_set_scroll_speed(game->back_layer2, f, f)
    land_layer_set_position(game->back_layer2, 0, h - 128)
    
    game->view->scroll_y = 0
    game->view->scroll_x = wave * wave_length * 64
    game->last_pos = game->view->scroll_x
    game->player = bee_new(game->view->scroll_x + 240, 240)
    if game->easy:
        game->player->lifes++
        game->next_life_score = 10000

    else:
        game->next_life_score = 25000
    game->start_wave = wave

def game_init(LandRunner *self):
    load()

static def honey():
    float x = LAND_SPRITE(game->player)->x + 200
    float y = LAND_SPRITE(game->player)->y + land_rand(-100, 100)
    honeypot_new(x, y)

def respawn():
    int wave = game->checkpoint
    if wave == game->start_wave and wave > 0:
        wave--
        
    int ns = game->next_life_score
    int s = game->score

    Being old = *game->player
    
    game_begin(wave, game->easy)

    game->next_life_score = ns
    game->score = s

    if game->easy == 1:
        if old.forward_shot > 1: honey()
        if old.down_shot > 1: honey()
        if old.triple_shot > 1: honey()
        if old.back_shot > 1: honey()

        if old.forward_shot > 2: honey()
        if old.down_shot > 2: honey()
        if old.triple_shot > 2: honey()
        if old.back_shot > 2: honey()


static def spawn():
    int i
    # Handle spawning of new enemies. 
    if game->view->scroll_x >= game->last_pos + 64:
        int l = game->last_pos / 64
        for i = 0 while i < 24 with i++:
            Being *b = NULL
            if waves[l][i] == 'F':
                int y = i * 32
                b = fly_new(game->view->scroll_x + 640 + 32, y)

            elif  waves[l][i] == 'f':
                int y = i * 32
                b = fly_new(game->view->scroll_x - 32, y)
                being_flip(b)

            elif  waves[l][i] == 'S':
                int y = i * 32
                b = strider_new(game->view->scroll_x + 640 + 32, y)

            elif  waves[l][i] == 's':
                int y = i * 32
                b = strider_new(game->view->scroll_x - 32, y)
                being_flip(b)

            elif  waves[l][i] == 'W':
                int y = i * 32
                b = wasp_new(game->view->scroll_x + 640 + 32, y)

            elif  waves[l][i] == 'w':
                int y = i * 32
                b = wasp_new(game->view->scroll_x - 32, y)
                being_flip(b)

            elif  waves[l][i] == 'M':
                int y = i * 32
                b = mosquito_new(game->view->scroll_x + 640 + 32, y)
                b->reload_ticker = 150

            elif  waves[l][i] == 'm':
                int y = i * 32
                b = mosquito_new(game->view->scroll_x - 32, y)
                b->reload_ticker = 150
                being_flip(b)

            elif  waves[l][i] == '<':
                int y = i * 32
                b = mosquito_new(game->view->scroll_x + 640 + 32, y)
                b->state = 1

            elif  waves[l][i] == '>':
                int y = i * 32
                b = mosquito_new(game->view->scroll_x + 640 + 32, y)
                b->state = -1

            if waves[l][i] == 'B':
                int y = i * 32
                b = beetle_new(game->view->scroll_x + 640 + 32, y)

            if waves[l][i] == 'b':
                int y = i * 32
                b = beetle_new(game->view->scroll_x - 32, y)
                being_flip(b)

            if waves[l][i] == 'L':
                int y = i * 32
                b = flea_new(game->view->scroll_x + 640 + 32, y)

            if waves[l][i] == 'l':
                int y = i * 32
                b = flea_new(game->view->scroll_x - 32, y)
                being_flip(b)

            if waves[l][i] == 'D':
                b = raindrop_new(game->view->scroll_x + 640 - i * 32, 0)

            if waves[l][i] == 'd':
                b = raindrop_new(game->view->scroll_x + 640 - i * 32, 32)

            if waves[l][i] == 'O':
                b = raindrop_new(game->view->scroll_x + 640 - i * 32, 64)

            if waves[l][i] == 'o':
                b = raindrop_new(game->view->scroll_x + 640 - i * 32, 96)

            if waves[l][i] == 'H':
                int y = i * 32
                b = hornet_new(game->view->scroll_x + 640 + 64, y)

            if waves[l][i] == '!':
                game->halt = 1
                game->boss = 1

            if waves[l][i] == '^':
                game->halt = 1
                game->won = 1

            if waves[l][i] == '@':
                b = leaf_new(game->view->scroll_x + 640 - i * 32, 0)

            elif  waves[l][i] == '*':
                game->target_scroll_y = i * 32

            elif  waves[l][i] == '~':
                game->water = 1

            elif  waves[l][i] == '_':
                game->water = 0

            elif  waves[l][i] == '{':
                game->wind = 1

            elif  waves[l][i] == '}':
                game->wind = 0

            elif  waves[l][i] == '0':
                if waves[l][i + 1] >= '1' and waves[l][i+1] <= '9':
                    game->group_active[waves[l][i + 1] - '0'] = 1


            if b and waves[l][i + 1] >= '1' and waves[l][i + 1] <= '9':
                b->group = waves[l][i + 1] - '0'
                game->group_count[b->group]++


        game->last_pos = game->view->scroll_x
        
        if waves[l][24]:
            message = waves[l] + 24
            message_time = 0



static def handle_input():
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape):
        if game->recording_active:
            #PACKFILE *pf = pack_fopen("recording", "wb")
            #pack_fwrite(game->recording, game->recording_pos, pf)
            #pack_fclose(pf)
            pass

        land_runner_switch_active(shortcut_runner)

    game->kx = 0
    game->ky = 0
    game->kf = 0
    
    if land_key_pressed(controls[5]) and game->game_over:
        respawn()
        return

    if land_key_pressed(controls[5]) and game->won:
        land_runner_switch_active(shortcut_runner)
        return

    if game->playback_active:
        if game->playback_pos == 0:
            pass
            # game->playback_allocated = file_size_ex("recording")
            # game->playback = malloc(game->playback_allocated)
            #PACKFILE *pf = pack_fopen("recording", "rb")
            # if pf:
            #    pack_fread(game->playback, game->playback_allocated, pf)
            #    pack_fclose(pf)


        if game->playback_pos < game->playback_allocated:
            int k = game->playback[game->playback_pos++]
            if k & 1: game->kx -= 1
            if k & 2: game->kx += 1
            if k & 4: game->ky -= 1
            if k & 8: game->ky += 1
            if k & 16: game->kf = 1


    else:
        if land_key(controls[1]): game->kx -= 1
        if land_key(controls[2]): game->kx += 1
        if land_key(controls[3]): game->ky -= 1
        if land_key(controls[4]): game->ky += 1
        if land_key(controls[5]): game->kf = 1

    if game->recording_active:
        int k = 0
        if game->kx < 0: k |= 1
        if game->kx > 0: k |= 2
        if game->ky < 0: k |= 4
        if game->ky > 0: k |= 8
        if game->kf: k |= 16
        if game->recording_pos >= game->recording_allocated:
            game->recording_allocated += 1024 * 1024
            game->recording = realloc(game->recording, game->recording_allocated)

        game->recording[game->recording_pos++] = k

    if game->kx > 1: game->kx = 1
    if game->kx < -1: game->kx = -1
    if game->ky > 1: game->ky = 1
    if game->ky < -1: game->ky = -1

#
   # if land_key_pressed(KEY_F1): game->player->back_shot++
   # if land_key_pressed(KEY_F2): game->player->down_shot++
   # if land_key_pressed(KEY_F3): game->player->triple_shot++
   # if land_key_pressed(KEY_F4): game->player->forward_shot++
   # if land_key_pressed(KEY_F5): game->player->shield++
#

def game_tick(LandRunner *self):
    handle_input()
    message_time++
    
    if game->player->dead:
        game->game_over++
        return

    if game->won:
        game->won++
        return

    # Move all beings in the game, including the player. 
    if game->beings:
        LandListItem *item, *next
        for item = game->beings->first while item with item = next:
            next = item->next
            Being *being = item->data
            being->tick(being)

        if game->player->dead: return
        
        # Destroy all beings who died in this tick. Doing an extra pass
        # immediately - probably could just check at the next tick as
        # well.
        #
        for item = game->beings->first while item with item = next:
            next = item->next
            Being *being = item->data
            if being->dead:
                land_list_remove_item(game->beings, item)
                land_free(item)
                being_destroy(being)



    spawn()

    if game->view->scroll_y < game->target_scroll_y:
        game->view->scroll_y += 0.5
    elif  game->view->scroll_y > game->target_scroll_y:
        game->view->scroll_y -= 0.5

    # Auto-scroll 1 pixel / tick 
    if not game->halt:
        game->view->scroll_x += 1.0

    land_view_ensure_inside_grid(game->view, game->middle_layer->grid)
    
    if game->score > game->next_life_score:
        game->next_life_score += 25000
        game->player->lifes++

    if not game->player->falling:
        game->checkpoint = game->last_pos / 6400

    # Handle foreground sprites animation. 
    float x = game->view->scroll_x * game->front_layer->scrolling_x
    float y = game->view->scroll_y
    LandList *backlist = land_sprites_grid_get_rectangle(
        game->front_layer->grid, x, y, x + 640, y + 480)
    if backlist:
        LandListItem *item
        for item = backlist->first while item with item = item->next:
            Being *back = item->data
            back->tick(back)

        land_list_destroy(backlist)

    # Handle background tiles animation. 
    int i
    float x1 = game->view->scroll_x * game->back_layer2->scrolling_x
    float x2 = x1 + game->view->w
    int j = (game->frame / 8) & 7
    int i1 = x1 / game->back_layer2->grid->cell_w
    int i2 = x2 / game->back_layer2->grid->cell_w
    for i = i1 while i <= i2 with i++:
        land_tilegrid_place(game->back_layer2->grid, i, 0,
            land_array_get_nth(backgrass[j], i & 7))

    # Ground 
    j = (game->frame / 4) & 15
    for i = 0 while i < game->back_layer3->grid->x_cells with i++:
        land_tilegrid_place(game->back_layer3->grid, i, 0,
            game->water ? land_array_get_nth(backdrop2, j) : backearth)

    if game->playback_active == 2:
        if not capture_frame:
            capture_frame = land_image_new(640, 480)

        if (game->playback_pos & 3) == 0:
            game_draw(self)
            land_image_grab(capture_frame, 0, 0)
            char str[256]
            snprintf(str, sizeof(str), "frames/frame%05d.tga", game->playback_pos / 4)
            # land_image_allegrogl_cache(capture_frame)
            # save_bitmap(str, capture_frame->memory_cache, NULL)
            # land_skip_frames()


    game->frame++

def game_draw(LandRunner *self):
    int i

    land_map_draw(game->map, game->view)
    

    # Draw reflections over water. 
    if game->water:
        LandLayer *layers[] = {game->middle_layer, game->middle_layer2}
        for i = 0 while i < 2 with i++:
            LandList *list
            list = land_sprites_grid_get_in_view(layers[i]->grid,
                game->view, 0, 0, 0, 0)
            if list:
                float waterline = 64 * 12 - 110 - game->view->scroll_y
                land_clip_push()
                land_clip(0, waterline, 640, 480)
                LandListItem *item
                for item = list->first while item with item = item->next:
                    LandSprite *sprite = item->data
                    float vx = sprite->x - game->view->scroll_x
                    float vy = sprite->y - game->view->scroll_y
                    
                    float y = waterline - vy
                    float a = (game->frame % (int)game->FPS) * LAND_PI * 2 /\
                        game->FPS
                    y = waterline + y
                    if y < vy + 32: y = vy + 32
                    if y > 480: continue
    
                    glPushMatrix()
                    glTranslatef(vx, y, 0)
                    glScalef(1 + cos(a) * 0.1, -0.9 + sin(a) * 0.2, 1)
                    glTranslatef(-vx, -vy, 0)
                    float backup = LAND_SPRITE_ANIMATED(sprite)->a
                    LAND_SPRITE_ANIMATED(sprite)->a = 0.5
                    sprite->type->draw(sprite, game->view)
                    LAND_SPRITE_ANIMATED(sprite)->a = backup
                    glPopMatrix()

                land_clip_pop()
                land_list_destroy(list)

    if game->player->dead:
        if game->game_over > 60:
            float a = game->game_over - 60
            a /= 360
            if a > 1: a = 1
            land_color(0, 0, 0, a)
            land_filled_rectangle(0, 0, 640, 480)

        land_text_pos(320, 200)
        land_color(1, 0, 0, 1)
        land_print_center("Game Over")
        land_text_pos(320, 280)
        land_color(0.5, 0, 0, 0.9)
        int wave = game->last_pos / 6400
        if wave == game->start_wave and wave > 0: wave--
        land_print_center("Press Fire")
        land_print_center("to restart in wave %d", 1 + wave)

    elif  game->won:
        float a = game->won
        a /= 360
        if a > 1: a = 1
        land_color(0, 0, 0, a)
        land_filled_rectangle(0, 0, 640, 480)

        land_text_pos(320, 200)
        land_color(1, 1, 0, 1)
        land_print_center("The End")

    if message and message_time < 360:
        char lines[16][256]
        int lines_count = 0
        char const *ptr = message
        int n = 0
        for i = 0 while i < (int)strlen(message) with i++:
            if message[i] == '\\':
                strncpy(lines[lines_count], ptr, 256)
                ptr += n + 1
                n = 0
                lines_count++

            else:
                n++

        strncpy(lines[lines_count], ptr, 256)
        lines_count++
        float a = message_time / 360.0
        a = sin(LAND_PI * a)
        int th = land_text_height()
        land_text_pos(320, 200 - th * lines_count / 2)
        land_color(1, 1, 1, a)
        for i = 0 while i < lines_count with i++:
            land_print_center(lines[i])

    land_font_set(tinyfont)
    land_color(1, 1, 1, 1)
    land_text_pos(0, 0)
    land_print("FPS: %.1f", game->fps)
    
    # land_text_pos(0, 80)
    # for i = 1 while i < 10 with i++:
    # {
    #     land_print("%d: %d %d+%d/%d", i, game->group_active[i],
    #         game->group_out[i], game->group_hit[i], game->group_count[i])
    # }

    land_font_set(menufont)
    land_color(1, 0.5, 0, 1)
    land_text_pos(0, 0)
    land_print("Score: %d", game->score)

    # Draw lifes and pots. 
    LandImage *beepic = land_animation_get_frame(LAND_SPRITE_TYPE_ANIMATION(
        LAND_SPRITE(game->player)->type)->animation, 0)
    for i = 0 while i < game->player->lifes with i++:
        land_image_draw_scaled(beepic, 640 - 16 - i * 32, 16, 0.5, 0.5)

    for i = 0 while i < game->player->pots with i++:
        land_image_draw_scaled(honeypot_frame(0), 640 - 16 - i * 32,
            16 + 32, 0.5, 0.5)

    if game->boss:
        # Draw boss health 
        int lifes = 0
        Being *boss = NULL
        LandList *list
        list = land_sprites_grid_get_in_view(game->middle_layer->grid,
            game->view, 0, 0, 0, 0)
        if list:
            LandListItem *item
            for item = list->first while item with item = item->next:
                boss = item->data
                if boss->bt == BT_HORNET:
                    lifes = boss->lifes
                    break


            land_list_destroy(list)

        if lifes:
            land_clip_push()
            land_clip(0, 0, lifes, 480)
            for i = 0 while i < 640 with i += 10:
                land_color(1 - i / 640.0, i / 640.0, 0, 0.6)
                land_filled_circle(i, 470, i + 10, 480)

            land_clip_pop()


    else:
        # Draw level overview. 
        land_color(0, 1, 0, 0.4)
        int w = game->middle_layer->grid->cell_w *\
            game->middle_layer->grid->x_cells - game->view->w
        land_filled_rectangle(0, game->view->h - 6,
            game->view->scroll_x * game->view->w / w,
            game->view->h)
    
        for i = 1 while i < 12 with i++:
            float x = i * game->view->w / 12
            land_line(x, game->view->h - 6, x, game->view->h)


    # FPS counter. 
    game->fps_accumulator++
    double t = land_get_time()
    if t - game->fps_time >= 1:
        game->fps = game->fps_accumulator / (t - game->fps_time)
        game->fps_accumulator = 0
        game->fps_time = t


def game_enter(LandRunner *self):
    land_hide_mouse_cursor()

def game_leave(LandRunner *self):
    land_show_mouse_cursor()

LandRunner * def game_register():
    LandRunner *runner = land_runner_new("game", game_init, game_enter,
        game_tick, game_draw, game_leave, NULL)
    land_runner_register(runner)
    return runner
