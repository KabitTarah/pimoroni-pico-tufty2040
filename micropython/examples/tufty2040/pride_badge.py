# A name badge with customisable Pride flag background.

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time

from util.button_handler import ButtonHandler
from util.constants import Constants as c
from util.wrapped_generator import WrappedGenerator

buttons = ButtonHandler()
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

WIDTH, HEIGHT = display.get_bounds()

# List of available pen colours, add more if necessary
RED = display.create_pen(209, 34, 41)
ORANGE = display.create_pen(246, 138, 30)
YELLOW = display.create_pen(255, 216, 0)
GREEN = display.create_pen(0, 121, 64)
INDIGO = display.create_pen(36, 64, 142)
VIOLET = display.create_pen(115, 41, 130)
WHITE = display.create_pen(255, 255, 255)
PINK = display.create_pen(255, 175, 200)
BLUE = display.create_pen(116, 215, 238)
BROWN = display.create_pen(97, 57, 21)
BLACK = display.create_pen(0, 0, 0)
MAGENTA = display.create_pen(255, 33, 140)
CYAN = display.create_pen(33, 177, 255)

# Uncomment one of these to change flag
# If adding your own, colour order is left to right (or top to bottom)
COLOUR_ORDERS = [
    [RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET],  # traditional pride flag
    [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET],  # Philadelphia pride flag
    [BLUE, PINK, WHITE, PINK, BLUE],  # trans flag
    [MAGENTA, YELLOW, CYAN],  # pan flag
    [MAGENTA, VIOLET, INDIGO], # bi flag
]

COLORS = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    INDIGO,
    VIOLET,
    WHITE,
    PINK,
    BLUE,
    BROWN,
    BLACK,
    MAGENTA,
    CYAN,
]

# Change this for vertical stripes
STRIPES_DIRECTIONS = ["horizontal", "vertical"]

# Change details here! Works best with a short, one word name
NAMES = ["Kabit", "Zee"]
PRONOUNS = ["She/It", "She/Her"]

# Change the colour of the text (swapping these works better on a light background)
TEXT_COLOUR = VIOLET
DROP_SHADOW_COLOUR = BLACK


def draw_flag(color_order, stripes_direction):
    # Draw the flag
    if stripes_direction == "horizontal":
        stripe_width = round(HEIGHT / len(color_order))
        for x in range(len(color_order)):
            display.set_pen(color_order[x])
            display.rectangle(0, stripe_width * x, WIDTH, stripe_width)

    elif stripes_direction == "vertical":
        stripe_width = round(WIDTH / len(color_order))
        for x in range(len(color_order)):
            display.set_pen(color_order[x])
            display.rectangle(stripe_width * x, 0, stripe_width, HEIGHT)
    
    else:
        raise Exception(f"{stripes_direction} not valid")


# These loops adjust the scale of the text until it fits on the screen
def set_name(name, text_color):
    # Set a starting scale for text size.
    # This is intentionally bigger than will fit on the screen, we'll shrink it to fit.
    name_size = 20

    while True:
        display.set_font("bitmap8")
        name_length = display.measure_text(name, name_size)
        if name_length >= WIDTH - 20:
            name_size -= 1
        else:
            # comment out this section if you hate drop shadow
            DROP_SHADOW_OFFSET = 5
            display.set_pen(DROP_SHADOW_COLOUR)
            display.text(name, int((WIDTH - name_length) / 2 + 10) - DROP_SHADOW_OFFSET, 10 + DROP_SHADOW_OFFSET, WIDTH, name_size)

            # draw name and stop looping
            display.set_pen(text_color)
            display.text(name, int((WIDTH - name_length) / 2 + 10), 10, WIDTH, name_size)
            break


def set_pronouns(pronouns, text_color):
    pronouns_size = 20

    while True:
        display.set_font("bitmap8")
        pronouns_length = display.measure_text(pronouns, pronouns_size)
        if pronouns_length >= WIDTH - 60:
            pronouns_size -= 1
        else:
            # draw pronouns and stop looping
            display.set_pen(text_color)
            display.text(pronouns, int((WIDTH - pronouns_length) / 2), 175, WIDTH, pronouns_size)
            break


# Once all the adjusting and drawing is done, update the display.
name_gen = WrappedGenerator(NAMES)
name = name_gen.next()
pronouns_gen = WrappedGenerator(PRONOUNS)
pronouns = pronouns_gen.next()
text_color_gen = WrappedGenerator(COLORS)
text_color = text_color_gen.next()
color_gen = WrappedGenerator(COLOUR_ORDERS)
color_order = color_gen.next()
direction_gen = WrappedGenerator(STRIPES_DIRECTIONS)
stripes_direction = direction_gen.next()

changed = True
while True:
    flags = buttons.get_flags()
    if "a" in flags and "c" in flags:
        break
    if changed:
        display.clear()
        draw_flag(color_order, stripes_direction)
        set_name(name, text_color)
        set_pronouns(pronouns, text_color)
        display.update()
        changed = False
        
    if buttons.get_flag("a"):
        name = name_gen.next()
        changed = True
    if buttons.get_flag("b"):
        text_color = text_color_gen.next()
        changed = True
    if buttons.get_flag("c"):
        pronouns = pronouns_gen.next()
        changed = True
    if buttons.get_flag("u"):
        color_order = color_gen.next()
        changed = True
    if buttons.get_flag("d"):
        stripes_direction = direction_gen.next()
        changed = True
    
    buttons.reset()

     # Allow for multiple button presses to control exit condition
    time.sleep_ms(250)
