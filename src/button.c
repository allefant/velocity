#ifdef _PROTOTYPE_

#include <land.h>

typedef struct Button Button;
struct Button
{
    Widget super;
    char *text;
    void (*cb)(Button *self);
    int key;
    int hilite;
};

extern int button_scroll;

#define BUTTON(_) ((Button *)(_))

#endif /* _PROTOTYPE_ */

#include "menu.h"
#include "button.h"
#include "game.h"

int button_scroll = 0;

static WidgetInterface *interface = NULL;

static LandImage *button_image;

static void mouse(Widget *self)
{
    Button *button = BUTTON(self);
    if ((land_mouse_delta_b() & 1)  && !(land_mouse_b() & 1))
    {
        if (button->cb) button->cb(button);
    }
}

static void enter(Widget *self)
{
    LandListItem *i;
    play_sample(sound->sho, 190, 128, 800, 0);
    for (i = WIDGET_CONTAINER(self->parent)->children->first; i; i = i->next)
        BUTTON(i->data)->hilite = 0;
    BUTTON(self)->hilite = 1;
}
static void leave(Widget *self) {BUTTON(self)->hilite = 0;}

static void draw(Widget *self)
{
    Button *button = BUTTON(self);
    int w = land_image_width(button_image);
    int h = land_image_height(button_image);
    int th = land_font_height(menufont);
    int x = self->box.x + button_scroll;
    if (button->hilite)
    {
        land_image_draw(button_image, x, self->box.y);
        land_color(0.9, 0.8, 0, 1);
    }
    else
    {
        land_image_draw_tinted(button_image, x, self->box.y,
            1, 1, 1, 0.5);
        land_color(0.9, 0.5, 0, 0.5);
    }

    if (button->key)
    {
        land_text_pos(x + w / 2, self->box.y + (h - th) / 2);
        
        land_print_center(scancode_to_name(controls[button->key]));
    }
    else
    {
        land_text_pos(x + w / 2, self->box.y + (h - th) / 2);
        land_print_center(BUTTON(self)->text);
    }
}

static void initialize(void)
{
    button_image = land_image_load("data/button.png");
    land_alloc(interface);
    interface->name = "button";
    interface->draw = draw;
    interface->mouse_tick = mouse;
    interface->mouse_enter = enter;
    interface->mouse_leave = leave;
}

Button *button_new(Widget *parent, int x, int y, char const *text,
    void (*cb)(Button *self))
{
    Button *self;
    if (!interface)
        initialize();
    land_alloc(self);
    int w = land_image_width(button_image);
    int h = land_image_height(button_image);
    widget_base_initialize(&self->super, parent, x - w / 2, y - h / 2, w, h);

    self->super.dont_clip = 1;
    self->super.vt = interface;
    self->text = ustrdup(text);
    self->cb = cb;
    return self;
}


