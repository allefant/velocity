import global land/land

import menu
import button
import game
import velocity

LandWidget *desktop, *old
LandWidget *mainmenu, *controlsmenu, *optionsmenu, *videomenu, *audiomenu,\
    *startmenu

float music_volume = 1

int cheat = 0
int start_wave = 0
int cheatcode[] = {'v', 'e', 'l', 'o', 'c', 'i', 't', 'y'};

static int game_running = 0

static int set_control = 0

static int scrolling = 0

static Button *fullscreen_button, *music_button, *start_option_button

static int start_option = 0

static float text_scoller_pos = 320
char const scroller_text[] = (
    "                                   "
    "******* Velocity the Bee *******"
    "    "
    "SHMUP 2006 Entry"
    "    "
    "by Allefant"
    "    "
    "*******"
    "    "
    "Ported from Amiga by Allefant Games"
    "    "
    "******"
    "    "
    "Greetings go to"
    "    "
    "*******"
    "    "
    "X-Out"
    "    "
    "*******"
    "    "
    "DrPetter"
    "    "
    "*******"
    "    "
    "Geecee3"
    "    "
    "*******"
    "    "
    "MarkR"
    "    "
    "*******"
    "    "
    "everyone else from #shmup"
    "    "
    "*******"
    "    "
    "Paul \"Madgarden\" Pridham"
    "    "
    "*******"
    "    "
    "Shawn Hargreaves"
    "    "
    "*******"
    "    "
    "George \"gfoot\" Foot"
    "    "
    "*******"
    "    "
    "Peter \"tjaden\" Wang"
    "    "
    "*******"
    "    "
    "Evert Glebbeek"
    "    "
    "*******"
    "    "
    "Eric Botcazou"
    "    "
    "*******"
    "    "
    "Robert \"Bob\" Ohannesian"
    "    "
    "*******"
    "    "
    "Ben \"entheh\" Davis"
    "    "
    "*******"
    "    "
    "various people from #allegro and www.allegro.cc"
    "    "
    "*******"
    "    "
    "the [AD] Mailing List"
    "    "
    "*******"
    "    "
    "everyone else I forgot"
    "    "
    "******"
    "    "
    "Visit our BBS!"
    "    "
    "http:# allefant.sf.net/Velocity"
    "    "
    "allefant@gmail.com"
    "    "
    "No cheatcodes available"
    "                                   ")

int music_on
global LandFont *tinyfont
global LandFont *menufont
global int controls[6]
char const *control_names[] = {"None", "Left", "Right", "Up", "Down", "Fire"}

LandRunner *run_game

#DUH *myduh
#AL_DUH_PLAYER *dumb

static def set_start_options():
    if start_option == 3:
        game->playback_active = 2
    
    if start_option == 2:
        game->recording_active = 1
        
    if start_option == 1:
        game->playback_active = 1

static def start_easy(Button *self):
    land_runner_switch_active(run_game)
    game_begin(start_wave, 1)
    land_skip_frames()
    game_running = 1
    
    set_start_options()

static def start_normal(Button *self):
    land_runner_switch_active(run_game)
    game_begin(start_wave, 0)
    land_skip_frames()
    game_running = 1
    
    set_start_options()

static def cont(Button *self):
    if game_running:
        land_runner_switch_active(run_game)
        land_skip_frames()


static def quit(Button *self):
    land_quit()

static def start(Button *self):
    desktop = startmenu
static def video(Button *self):
    desktop = videomenu
static def audio(Button *self):
    desktop = audiomenu
static def backcontrols(Button *self):
    desktop = controlsmenu
static def backmain(Button *self):
    desktop = mainmenu
static def backoptions(Button *self):
    desktop = optionsmenu
static def control(Button *self):
    set_control = self->key
static def check_fullscreen():
    free(fullscreen_button->text)
    fullscreen_button->text = land_strdup(
        (land_display_get()->flags & LAND_FULLSCREEN) ?
        "Windowed" : "Fullscreen")
    land_ini_set_int(ini, "video", "fullscreen",
        !!(land_display_get()->flags & LAND_FULLSCREEN))

static def check_startoption():
    free(start_option_button->text)
    start_option_button->text = land_strdup(
        start_option == 3 ? "Video" :
        start_option == 2 ? "Record" :
        start_option == 1 ? "Playback" : "")

static def startoption(Button *self):
    start_option++
    start_option %= 4
    check_startoption()

#  HACK HACK HACK
#class AL_DUH_PLAYER:
#    int flags
#    long bufsize
#    int freq
#    AUDIOSTREAM *stream
#    DUH_SIGRENDERER *sigrenderer
#    float volume
#    int silentcount

#static def blah():
#    al_poll_duh(dumb)

#static def playdumb():
#    remove_int(blah)
#    if dumb: al_stop_duh(dumb)
#    dumb = al_start_duh(myduh, music_volume, 0, (double)2, 4096, 48000)
#    voice_set_volume(dumb->stream->voice, 180)
#    install_int_ex(blah, BPS_TO_TIMER(100))

#  HACK HACK HACK


static def fullscreen(Button *self):
    land_display_toggle_fullscreen()
    land_show_mouse_cursor()
    check_fullscreen()

    #playdumb()

static def check_music():
    land_free(music_button->text)
    music_button->text = land_strdup(
        music_on ?
        "Music Off" : "Music On")
    land_ini_set_int(ini, "audio", "music", music_on)

    # if not music_on: al_pause_duh(dumb)
    # else al_resume_duh(dumb)

static def music(Button *self):
    music_on ^= 1
    check_music()

def menu_init(LandRunner *self):
    Button *b

    controls[1] = land_ini_get_int(ini, "controls", control_names[1], LandKeyLeft)
    controls[2] = land_ini_get_int(ini, "controls", control_names[2], LandKeyRight)
    controls[3] = land_ini_get_int(ini, "controls", control_names[3], LandKeyUp)
    controls[4] = land_ini_get_int(ini, "controls", control_names[4], LandKeyDown)
    controls[5] = land_ini_get_int(ini, "controls", control_names[5], LandKeyRightControl)

    mainmenu = land_widget_container_new(NULL, 0, 0, 640, 480)
    mainmenu->dont_clip = 1
    button_new(mainmenu, 320, 180, "Continue", cont)
    button_new(mainmenu, 320, 240, "Start", start)
    button_new(mainmenu, 320, 360, "Options", backoptions)
    button_new(mainmenu, 320, 420, "Quit", quit)
    
    startmenu = land_widget_container_new(NULL, 0, 0, 640, 480)
    startmenu->dont_clip = 1
    button_new(startmenu, 320, 180, "Easy game", start_easy)
    button_new(startmenu, 320, 240, "Normal game", start_normal)
    start_option_button = button_new(startmenu, 320, 300, "", startoption)
    button_new(startmenu, 320, 360, "Back", backmain)
    
    check_startoption()
    
    optionsmenu = land_widget_container_new(NULL, 0, 0, 640, 480)
    optionsmenu->dont_clip = 1
    button_new(optionsmenu, 320, 180, "Video", video)
    button_new(optionsmenu, 320, 240, "Audio", audio)
    button_new(optionsmenu, 320, 300, "Controls", backcontrols)
    button_new(optionsmenu, 320, 360, "Back", backmain)

    videomenu = land_widget_container_new(NULL, 0, 0, 640, 480)
    videomenu->dont_clip = 1
    fullscreen_button = button_new(videomenu, 320, 180, "", fullscreen)
    button_new(videomenu, 320, 360, "Back", backoptions)

    audiomenu = land_widget_container_new(NULL, 0, 0, 640, 480)
    audiomenu->dont_clip = 1
    music_button = button_new(audiomenu, 320, 180, "", music)
    button_new(audiomenu, 320, 360, "Back", backoptions)

    controlsmenu = land_widget_container_new(NULL, 0, 0, 640, 480)
    controlsmenu->dont_clip = 1
    b = button_new(controlsmenu, 320, 60, "", control)
    b->key = 1
    b = button_new(controlsmenu, 320, 120, "", control)
    b->key = 2
    b = button_new(controlsmenu, 320, 180, "", control)
    b->key = 3
    b = button_new(controlsmenu, 320, 240, "", control)
    b->key = 4
    b = button_new(controlsmenu, 320, 300, "", control)
    b->key = 5
    button_new(controlsmenu, 320, 360, "Back", backoptions)
    
    run_game = game_register()
    
    menufont = land_font_load("data/beefont.png", 1)
    
    #install_sound(DIGI_AUTODETECT, MIDI_NONE, NULL)

    #int size
    #char *mem = land_datafile_read_entry(land_get_datafile(), "data/beesong.xm", &size)
    # if mem:
    #    DUMBFILE *df = dumbfile_open_memory(mem, size)
    #    if df:
    #        myduh = dumb_read_xm(df)


    # if not myduh:
    #    myduh = dumb_load_xm_quick("data/beesong.xm")

    music_on = land_ini_get_int(ini, "audio", "music", 1)

    #playdumb()

    check_music()
    # install_int_ex(blah, BPS_TO_TIMER(100))
    check_fullscreen()
    
    old = desktop = mainmenu

static def move_hilite(int dir):
    LandListItem *i
    land_sound_play(sound->sho, 0.75, 0, 0.8)
    for i = LAND_WIDGET_CONTAINER(desktop)->children->first while i with i = i->next:
        if BUTTON(i->data)->hilite:
            BUTTON(i->data)->hilite = 0
            if dir == -1:
                if i->prev:
                    BUTTON(i->prev->data)->hilite = 1
                else:
                    while i->next: i = i->next
                    BUTTON(i->data)->hilite = 1


            if dir == 1:
                if i->next:
                    BUTTON(i->next->data)->hilite = 1
                else:
                    while i->prev: i = i->prev
                    BUTTON(i->data)->hilite = 1


            return


    BUTTON(LAND_WIDGET_CONTAINER(desktop)->children->first->data)->hilite = 1

static def activate():
    LandListItem *i
    for i = LAND_WIDGET_CONTAINER(desktop)->children->first while i with i = i->next:
        if BUTTON(i->data)->hilite:
            BUTTON(i->data)->cb(i->data)
            return



def menu_tick(LandRunner *self):
    if land_closebutton(): land_quit()
    
    text_scoller_pos += 2

    if set_control:
        if land_key_pressed(LandKeyEscape):
            set_control = 0
            return

        int k
        for k = 1 while k < LandKeysCount with k++:
            if land_key_pressed(k):
                controls[set_control] = k
                land_ini_set_int(ini, "controls", control_names[set_control], k)
                set_control = 0


        return

    if land_key_pressed(LandKeyEscape):
        scrolling = 0

    int i
    if cheat < 8:
        for i = 1 while i < LandKeysCount with i++:
            if land_key_pressed(i):
                if cheatcode[cheat] == i:
                    cheat++
                    if cheat == 8:
                        land_sound_play(sound->tat, 1, 0, 1)


                else:
                    cheat = 0



    else:
        for int wi = 0 while wi < 9 with wi++:
            if land_key_pressed('1' + wi): start_wave = 2 + wi
        if land_key_pressed('0'): start_wave = 11

    if not scrolling:
        old = desktop
        int dx = 0
        if land_key_pressed(LandKeyLeft): dx -= 1
        if land_key_pressed(LandKeyRight): dx -= 1
        
        if desktop == startmenu:
            start_option += dx
            start_option %= 4
            if start_option < 0: start_option += 4
            check_startoption()

        if land_key_pressed(LandKeyUp): move_hilite(-1)
        if land_key_pressed(LandKeyDown): move_hilite(1)
        if land_key_pressed(LandKeyEnter) or land_key_pressed(' ') or\
            land_key_pressed(controls[5]):
            activate()

        desktop->vt->mouse_tick(desktop)
        
        if land_key_pressed(LandKeyEscape):
            if desktop == mainmenu: land_quit()
            elif  desktop == optionsmenu || desktop == startmenu:
                desktop = mainmenu
            else desktop = optionsmenu

        if old != desktop:
            land_sound_play(sound->bom, 1, 0, 1)
            if desktop == mainmenu: scrolling = 640
            elif  desktop == controlsmenu: scrolling = -640
            elif  desktop == videomenu or desktop == audiomenu:
                scrolling = -640
            elif  old == mainmenu: scrolling = -640
            elif  old == controlsmenu or old == videomenu or old == audiomenu:
                scrolling = 640

    else:
        if scrolling > 0: scrolling -= 20
        if scrolling < 0: scrolling += 20


static def draw_controls():
    int th = land_font_height(menufont)
    int i
    land_color(0, 0, 0, 0.5)
    for i = 1 while i < 6 with i++:
        land_text_pos(0, button_scroll + i * 60 - th / 2)
        land_print(control_names[i])


static float def function(float x):
    return 64 * sin((x + 100) / 90)

static def draw_text_scroller():
    float x
    int i = 0
    float s = 32
    x = -text_scoller_pos
    while x < 640 + 32:
        float vx = s
        float vy = function(x + vx) - function(x)
        float v = sqrt(vx * vx + vy * vy)
        vx = vx * s / v
        vy = vy * s / v
        float nx = vy
        float ny = -vx
        float a = atan2(nx, ny)
        float y = 90 + function(x)
        if x > -32:
            int ri, gi, bi
            # hsv_to_rgb(i * 10, 1, 1, &ri, &gi, &bi)
            float alpha = 1 - fabs(x - 320) / 320.0
            land_color(ri / 255.0, gi / 255.0, bi / 255.0, alpha)
            char str[16]
            if scroller_text[i] == '\0':
                text_scoller_pos = 0
                i = 0

            str[0] = scroller_text[i]
            str[1] = 0
            glPushMatrix()
            glTranslatef(x, y, 0)
            glRotatef(-180 * a / LAND_PI + 180, 0, 0, 1)
            land_text_pos(0, -32)
            land_print_center(str)
            glPopMatrix()

        x += vx
        i++


static float def s(float x):
    return 640 - 640 * sin((640 - x) * LAND_PI / 2 / 640)

def menu_draw(LandRunner *self):
    land_font_set(menufont)
    
    draw_text_scroller()

    if set_control:
        land_text_pos(320, 200)
        land_color(1, 0, 0, 1)
        land_print_center("Press new key")
        land_print_center("for %s", control_names[set_control])
        return

    if scrolling < 0:
        button_scroll = s(-scrolling) - 640
        land_widget_draw(old)
        button_scroll = s(-scrolling)

    elif  scrolling > 0:
        button_scroll = 640 - s(scrolling)
        land_widget_draw(old)
        if old == controlsmenu: draw_controls()
        button_scroll = -s(scrolling)

    if desktop == controlsmenu: draw_controls()

    land_widget_draw(desktop)

def menu_exit(LandRunner *self):
    pass

LandRunner *def menu_register():
    LandRunner *runner = land_runner_new("menu", menu_init, None,
        menu_tick, menu_draw, None, menu_exit)
    land_runner_register(runner)
    return runner
