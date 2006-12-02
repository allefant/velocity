import global land

class Button:
    LandWidget super
    char *text
    void (*cb)(Button *self)
    int key
    int hilite

macro BUTTON(_) ((Button *)(_))

import menu
import button
import game

global int button_scroll = 0

static LandWidgetInterface *interface = NULL

static LandImage *button_image

static def mouse(LandWidget *self):
    Button *button = BUTTON(self)
    if (land_mouse_delta_b() & 1)  && !(land_mouse_b() & 1):
        if button->cb: button->cb(button)


static def enter(LandWidget *self, LandWidget *focus):
    LandListItem *i
    play_sample(sound->sho, 190, 128, 800, 0)
    for i = LAND_WIDGET_CONTAINER(self->parent)->children->first; i; i = i->next:
        BUTTON(i->data)->hilite = 0
    BUTTON(self)->hilite = 1

static def leave(LandWidget *self, LandWidget *focus):
    BUTTON(self)->hilite = 0

static def draw(LandWidget *self):
    Button *button = BUTTON(self)
    int w = land_image_width(button_image)
    int h = land_image_height(button_image)
    int th = land_font_height(menufont)
    int x = self->box.x + button_scroll
    if button->hilite:
        land_image_draw(button_image, x, self->box.y)
        land_color(0.9, 0.8, 0, 1)

    else:
        land_image_draw_tinted(button_image, x, self->box.y,
            1, 1, 1, 0.5)
        land_color(0.9, 0.5, 0, 0.5)

    if button->key:
        land_text_pos(x + w / 2, self->box.y + (h - th) / 2)

        land_print_center(scancode_to_name(controls[button->key]))

    else:
        land_text_pos(x + w / 2, self->box.y + (h - th) / 2)
        land_print_center(BUTTON(self)->text)


static def initialize():
    button_image = land_image_load("data/button.png")
    land_alloc(interface)
    interface->name = "button"
    interface->draw = draw
    interface->mouse_tick = mouse
    interface->mouse_enter = enter
    interface->mouse_leave = leave

Button *def button_new(LandWidget *parent, int x, y, char const *text,
    void (*cb)(Button *self)):
    Button *self
    if not interface:
        initialize()
    land_alloc(self)
    int w = land_image_width(button_image)
    int h = land_image_height(button_image)
    land_widget_base_initialize(&self->super, parent, x - w / 2, y - h / 2, w, h)

    self->super.dont_clip = 1
    self->super.vt = interface
    self->text = ustrdup(text)
    self->cb = cb
    return self
