from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
from pimoroni import Button


class Constants:
    display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)
    
    button_up = Button(22, invert=False)
    button_down = Button(6, invert=False)
    button_a = Button(7, invert=False)
    button_b = Button(8, invert=False)
    button_c = Button(9, invert=False)

