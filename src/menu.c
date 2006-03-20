#ifdef _PROTOTYPE_
#include <land.h>
extern LandFont *menufont;
extern LandFont *tinyfont;
extern int controls[6];

#endif /* _PROTOTYPE_ */

#include <aldumb.h>

#include "menu.h"
#include "button.h"
#include "game.h"

static LandWidget *desktop, *old;
static LandWidget *mainmenu, *controlsmenu, *optionsmenu, *videomenu,
    *audiomenu;

static float music_volume = 1;

static int cheat = 0;
static int start_wave = 0;
static int cheatcode[] = {KEY_V, KEY_E, KEY_L, KEY_O, KEY_C, KEY_I, KEY_T, KEY_Y};

static int game_running = 0;

static int set_control = 0;

static int scrolling = 0;

static Button *fullscreen_button, *music_button;

static float text_scoller_pos = 320;
char const scroller_text[] =
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
    "http://allefant.sf.net/Velocity"
    "    "
    "allefant@gmail.com"
    "    "
    "No cheatcodes available"
    "                                   ";

int music_on;
LandFont *tinyfont;
LandFont *menufont;
int controls[6];
char const *control_names[] = {"None", "Left", "Right", "Up", "Down", "Fire"};

LandRunner *run_game;

static DUH *myduh;
static AL_DUH_PLAYER *dumb;

static void start(Button *self)
{
    land_runner_switch_active(run_game);
    game_begin(start_wave, 1);
    land_skip_frames();
    game_running = 1;
}

static void start_normal(Button *self)
{
    land_runner_switch_active(run_game);
    game_begin(start_wave, 0);
    land_skip_frames();
    game_running = 1;
}

static void cont(Button *self)
{
    if (game_running)
    {
        land_runner_switch_active(run_game);
        land_skip_frames();
    }
}

static void quit(Button *self)
{
    land_quit();
}

static void video(Button *self) {desktop = videomenu;}
static void audio(Button *self) {desktop = audiomenu;}
static void backcontrols(Button *self) {desktop = controlsmenu;}
static void backmain(Button *self) {desktop = mainmenu;}
static void backoptions(Button *self) {desktop = optionsmenu;}
static void control(Button *self) {set_control = self->key;}
static void check_fullscreen(void)
{
    free(fullscreen_button->text);
    fullscreen_button->text = ustrdup(
        (land_display_get()->flags & LAND_FULLSCREEN) ?
        "Windowed" : "Fullscreen");
    set_config_int("video", "fullscreen",
        !!(land_display_get()->flags & LAND_FULLSCREEN));
}



// HACK HACK HACK
struct AL_DUH_PLAYER
{
	int flags;
	long bufsize;
	int freq;
	AUDIOSTREAM *stream;
	DUH_SIGRENDERER *sigrenderer;
	float volume;
	int silentcount;
};
static void blah(void) {al_poll_duh(dumb);}
static void playdumb(void)
{
    remove_int(blah);
    if (dumb) al_stop_duh(dumb);
    dumb = al_start_duh(myduh, music_volume, 0, (double)2, 4096, 48000);
    voice_set_volume(dumb->stream->voice, 180);
    install_int_ex(blah, BPS_TO_TIMER(100));
}
// HACK HACK HACK


static void fullscreen(Button *self)
{
    land_display_toggle_fullscreen();
    land_show_mouse_cursor();
    check_fullscreen();

    playdumb();
}

static void check_music(void)
{
    free(music_button->text);
    music_button->text = ustrdup(
        music_on ?
        "Music Off" : "Music On");
    set_config_int("audio", "music", music_on);

    if (!music_on) al_pause_duh(dumb);
    else al_resume_duh(dumb);
}

static void music(Button *self)
{
    music_on ^= 1;
    check_music();
}

void menu_init(LandRunner *self)
{
    Button *b;

    controls[1] = get_config_int("controls", control_names[1], KEY_LEFT);
    controls[2] = get_config_int("controls", control_names[2], KEY_RIGHT);
    controls[3] = get_config_int("controls", control_names[3], KEY_UP);
    controls[4] = get_config_int("controls", control_names[4], KEY_DOWN);
    controls[5] = get_config_int("controls", control_names[5], KEY_RCONTROL);

    mainmenu = widget_container_new(NULL, 0, 0, 640, 480);
    mainmenu->dont_clip = 1;
    button_new(mainmenu, 320, 180, "Continue", cont);
    button_new(mainmenu, 320, 240, "Easy game", start);
    button_new(mainmenu, 320, 300, "Normal game", start_normal);
    button_new(mainmenu, 320, 360, "Options", backoptions);
    button_new(mainmenu, 320, 420, "Quit", quit);
    
    optionsmenu = widget_container_new(NULL, 0, 0, 640, 480);
    optionsmenu->dont_clip = 1;
    button_new(optionsmenu, 320, 180, "Video", video);
    button_new(optionsmenu, 320, 240, "Audio", audio);
    button_new(optionsmenu, 320, 300, "Controls", backcontrols);
    button_new(optionsmenu, 320, 360, "Back", backmain);

    videomenu = widget_container_new(NULL, 0, 0, 640, 480);
    videomenu->dont_clip = 1;
    fullscreen_button = button_new(videomenu, 320, 180, "", fullscreen);
    button_new(videomenu, 320, 360, "Back", backoptions);

    audiomenu = widget_container_new(NULL, 0, 0, 640, 480);
    audiomenu->dont_clip = 1;
    music_button = button_new(audiomenu, 320, 180, "", music);
    button_new(audiomenu, 320, 360, "Back", backoptions);

    controlsmenu = widget_container_new(NULL, 0, 0, 640, 480);
    controlsmenu->dont_clip = 1;
    b = button_new(controlsmenu, 320, 60, "", control);
    b->key = 1;
    b = button_new(controlsmenu, 320, 120, "", control);
    b->key = 2;
    b = button_new(controlsmenu, 320, 180, "", control);
    b->key = 3;
    b = button_new(controlsmenu, 320, 240, "", control);
    b->key = 4;
    b = button_new(controlsmenu, 320, 300, "", control);
    b->key = 5;
    button_new(controlsmenu, 320, 360, "Back", backoptions);
    
    run_game = game_register();
    
    menufont = land_font_load("data/beefont.png", 1);
    
    install_sound(DIGI_AUTODETECT, MIDI_NONE, NULL);

    int size;
    char *mem = land_datafile_read_entry(land_get_datafile(), "data/beesong.xm", &size);
    if (mem)
    {
        DUMBFILE *df = dumbfile_open_memory(mem, size);
        if (df)
        {
            myduh = dumb_read_xm(df);
        }
    }
    if (!myduh)
        myduh = dumb_load_xm_quick("data/beesong.xm");

    music_on = get_config_int("audio", "music", 1);

    playdumb();

    check_music();
    install_int_ex(blah, BPS_TO_TIMER(100));
    check_fullscreen();
    
    old = desktop = mainmenu;
}

static void move_hilite(int dir)
{
    LandListItem *i;
    play_sample(sound->sho, 190, 128, 800, 0);
    for (i = WIDGET_CONTAINER(desktop)->children->first; i; i = i->next)
    {
        if (BUTTON(i->data)->hilite)
        {
            BUTTON(i->data)->hilite = 0;
            if (dir == -1)
            {
                if (i->prev)
                    BUTTON(i->prev->data)->hilite = 1;
                else
                {
                    while (i->next) i = i->next;
                    BUTTON(i->data)->hilite = 1;
                }
            }
            if (dir == 1)
            {
                if (i->next)
                    BUTTON(i->next->data)->hilite = 1;
                else
                {
                    while (i->prev) i = i->prev;
                    BUTTON(i->data)->hilite = 1;
                }
            }
            return;
        }
    }
    BUTTON(WIDGET_CONTAINER(desktop)->children->first->data)->hilite = 1;
}

static void activate(void)
{
    LandListItem *i;
    for (i = WIDGET_CONTAINER(desktop)->children->first; i; i = i->next)
    {
        if (BUTTON(i->data)->hilite)
        {
            BUTTON(i->data)->cb(i->data);
            return;
        }
    }
}

void menu_tick(LandRunner *self)
{
    if (land_closebutton()) land_quit();
    
    text_scoller_pos += 2;

    if (set_control)
    {
        if (land_key_pressed(KEY_ESC))
        {
            set_control = 0;
            return;
        }
        int k;
        for (k = 1; k < KEY_MAX; k++)
        {
            if (land_key_pressed(k))
            {
                controls[set_control] = k;
                set_config_int("controls", control_names[set_control], k);
                set_control = 0;
            }
        }
        return;
    }

    if (land_key_pressed(KEY_ESC))
    {
        scrolling = 0;
    }

    int i;
    if (cheat < 8)
    {
        for (i = 1; i < KEY_MAX; i++)
        {
            if (land_key_pressed(i))
            {
                if (cheatcode[cheat] == i)
                {
                    cheat++;
                    if (cheat == 8)
                    {
                        play_sample(sound->tat, 255, 128, 1000, 0);
                    }
                }
                else
                    cheat = 0;
            }
        }
    }
    else
    {
        if (land_key_pressed(KEY_1)) start_wave = 2;
        if (land_key_pressed(KEY_2)) start_wave = 3;
        if (land_key_pressed(KEY_3)) start_wave = 4;
        if (land_key_pressed(KEY_4)) start_wave = 5;
        if (land_key_pressed(KEY_5)) start_wave = 6;
        if (land_key_pressed(KEY_6)) start_wave = 7;
        if (land_key_pressed(KEY_7)) start_wave = 8;
        if (land_key_pressed(KEY_8)) start_wave = 9;
        if (land_key_pressed(KEY_9)) start_wave = 10;
        if (land_key_pressed(KEY_0)) start_wave = 11;
    }
    
    if (!scrolling)
    {
        old = desktop;
        if (land_key_pressed(KEY_UP)) move_hilite(-1);
        if (land_key_pressed(KEY_DOWN)) move_hilite(1);
        if (land_key_pressed(KEY_ENTER) || land_key_pressed(KEY_SPACE) ||
            land_key_pressed(controls[5]))
        {
            activate();
        }

        desktop->vt->mouse_tick(desktop);
        
        if (land_key_pressed(KEY_ESC))
        {
            if (desktop == mainmenu) land_quit();
            else if (desktop == optionsmenu) desktop = mainmenu;
            else desktop = optionsmenu;
        }
        
        if (old != desktop)
        {
            play_sample(sound->bom, 255, 128, 1000, 0);
            if (desktop == mainmenu) scrolling = 640;
            else if (desktop == controlsmenu) scrolling = -640;
            else if (desktop == videomenu || desktop == audiomenu)
                scrolling = -640;
            else if (old == mainmenu) scrolling = -640;
            else if (old == controlsmenu) scrolling = 640;
            else if (old == videomenu || old == audiomenu) scrolling = 640;
        }
    }
    else
    {
        if (scrolling > 0) scrolling -= 20;
        if (scrolling < 0) scrolling += 20;
    }
}

static void draw_controls(void)
{
    
    int th = land_font_height(menufont);
    int i;
    land_color(0, 0, 0, 0.5);
    for (i = 1; i < 6; i++)
    {
        land_text_pos(0, button_scroll + i * 60 - th / 2);
        land_print(control_names[i]);
    }
    
}

static float function(float x)
{
    return 64 * sin((x + 100) / 90);
}

static void draw_text_scroller(void)
{
    float x;
    int i = 0;
    float s = 32;
    x = -text_scoller_pos;
    while (x < 640 + 32)
    {
        float vx = s;
        float vy = function(x + vx) - function(x);
        float v = sqrt(vx * vx + vy * vy);
        vx = vx * s / v;
        vy = vy * s / v;
        float nx = vy;
        float ny = -vx;
        float a = atan2(nx, ny);
        float y = 90 + function(x);
        if (x > -32)
        {
            int ri, gi, bi;
            hsv_to_rgb(i * 10, 1, 1, &ri, &gi, &bi);
            float alpha = 1 - fabs(x - 320) / 320.0;
            land_color(ri / 255.0, gi / 255.0, bi / 255.0, alpha);
            char str[16];
            if (scroller_text[i] == '\0')
            {
                text_scoller_pos = 0;
                i = 0;
            }
            ustrzncpy(str, sizeof(str), scroller_text + i, 1);
            glPushMatrix();
            glTranslatef(x, y, 0);
            glRotatef(-180 * a / AL_PI + 180, 0, 0, 1);
            land_text_pos(0, -32);
            land_print_center(str);
            glPopMatrix();
        }
        x += vx;
        i++;
    }
}

static float s(float x)
{
    return 640 - 640 * sin((640 - x) * AL_PI / 2 / 640);
}

void menu_draw(LandRunner *self)
{
    land_font_set(menufont);
    
    draw_text_scroller();

    if (set_control)
    {
        land_text_pos(320, 200);
        land_color(1, 0, 0, 1);
        land_print_center("Press new key");
        land_print_center("for %s", control_names[set_control]);
        return;
    }

    if (scrolling < 0)
    {
        button_scroll = s(-scrolling) - 640;
        widget_draw(old);
        button_scroll = s(-scrolling);
    }
    else if (scrolling > 0)
    {
        button_scroll = 640 - s(scrolling);
        widget_draw(old);
        if (old == controlsmenu) draw_controls();
        button_scroll = -s(scrolling);
    }

    if (desktop == controlsmenu) draw_controls();

    widget_draw(desktop);
}

void menu_exit(LandRunner *self)
{
}

LandRunner *menu_register(void)
{
    LandRunner *runner = land_runner_new("menu", menu_init, NULL,
        menu_tick, menu_draw, NULL, menu_exit);
    land_runner_register(runner);
    return runner;
}
