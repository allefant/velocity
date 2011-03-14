# 
# One level is 76800 x 768 pixels big.
# One level has 12 waves, each one being 6400 pixels wide.
# The scroll speed is 100 pixel / second - so one wave takes 64 seconds.
# One level takes about 12 minutes (exact time would take into account the
# view width and time spent on bosses) 
#
# - level 1: river bank
#   fly, flea, mosquito, wasp, water strider, beetle, leaf
#   boss: hornet
#
# - level 2: night
#   glow worm, firefly, worm, spider
#   boss: cicada
#
# - level 3: icy
#   ice drop, snow flake
#   boss: ice wall
#
# - level 4: forest
#   beetle, leaf, needles
#   final boss: carnivorous plant
#
# - lit clouds at the floor, in several parallax layers
# - fog
#
# - try to split all textures to no more than 512x512
#

import global land/land

import being, menu

LandRunner *run_menu = NULL

global LandIniFile *ini

static LandArray *title

static int progress_meter = 0
static int images_count = 248

static def progress(char const *path, LandImage *image):
    progress_meter++
    int p = progress_meter * 41 / images_count
    land_font_set(tinyfont)
    land_color(1, 1, 1, 1)
    land_text_pos(320 - 21 * 6 + p * 6, 246)
    land_print(".")
    land_flip()

def ascii(char const *name, int xp, int yp):
    char *a = land_read_text(name)
    int s = strlen(a)

    land_color(1, 1, 1, 1)

    int i = 0
    for int y = 0 while with y++:
        for int x = 0 while with x++:
            if i == s:
                land_free(a)
                return

            int c = a[i++]
            if c == '\n':
                break

            land_text_pos(xp + x * 6, yp + y * 6)
            land_print("%c", c)

def main_init(LandRunner *self):
    ini = land_ini_read("velocity.cfg")
    if land_ini_get_int(ini, "video", "fullscreen", 0):
        land_display_toggle_fullscreen()

    land_show_mouse_cursor()
    land_clear(0, 0, 0, 0)

    LandDataFile *dat

    char name[1024] = "."
    # get_executable_name(name, sizeof(name))
    #dat = land_open_appended_datafile(name, "velocity")
    # if not dat: dat = land_open_appended_datafile("Velocity the Bee by Allefant.exe", "velocity")
    # if not dat: dat = land_open_datafile("velo.city")
    # if not dat:
    #    printf("Velocity the Bee - Error - No data found!")
    #    exit(-1)

    #land_set_datafile(dat)

    tinyfont = land_font_load("data/6x6.png", 1.0)

    ascii("data/story.txt", 6, 6)
    ascii("data/thanks.txt", 84 * 6, 6)
    ascii("data/smile.txt", 320 - 20 * 6, 6)
    ascii("data/logo.txt", 320 - 40 * 6, 51 * 6)

    land_text_pos(320, 240)
    land_color(1, 1, 1, 1)
    land_print_center("Loading")
    land_print_center("[                                          ]")
    
    land_flip()

    land_image_set_callback(progress)

    title = land_load_images("data/title_*", 0, 0)

    menu_init(self)
    game_init(self)

    if progress_meter != images_count:
        printf("expected %d images, got %d\n", images_count, progress_meter)
    land_image_set_callback(NULL)

def main_tick(LandRunner *self):
    menu_tick(self)

def main_draw(LandRunner *self):
    land_clear(1, 0, 0, 1)
    land_image_draw(land_array_get_nth(title, (land_get_ticks() / 4) & 15), 0, 0)

    menu_draw(self)

land_begin_shortcut(640, 480, 100,
    LAND_OPENGL | LAND_WINDOWED,
    main_init, NULL, main_tick, main_draw, NULL, NULL)
