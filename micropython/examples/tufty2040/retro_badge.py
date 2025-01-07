# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.

import gc
import os
from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
from pimoroni import Button
import time
import jpegdec
import qrcode

from util.button_handler import ButtonHandler
from util.constants import Constants as c
from util.wrapped_generator import WrappedGeneratorTimer

DISPLAY = c.display
WIDTH, HEIGHT = DISPLAY.get_bounds()

# Uncomment one of these four colour palettes - find more at lospec.com !
# Nostalgia colour palette by WildLeoKnight - https://lospec.com/palette-list/nostalgia
# LIGHTEST = DISPLAY.create_pen(208, 208, 88)
# LIGHT = DISPLAY.create_pen(160, 168, 64)
# DARK = DISPLAY.create_pen(112, 128, 40)
# DARKEST = DISPLAY.create_pen(64, 80, 16)

# 2bit Demichrome colour palette by Space Sandwich - https://lospec.com/palette-list/2bit-demichrome
# LIGHTEST = DISPLAY.create_pen(233, 239, 236)
# LIGHT = DISPLAY.create_pen(160, 160, 139)
# DARK = DISPLAY.create_pen(85, 85, 104)
# DARKEST = DISPLAY.create_pen(33, 30, 32)

# CGA PALETTE 1 (HIGH) - https://lospec.com/palette-list/cga-palette-1-high
# LIGHTEST = DISPLAY.create_pen(255, 255, 255)
# LIGHT = DISPLAY.create_pen(85, 254, 255)
# DARK = DISPLAY.create_pen(255, 85, 255)
# DARKEST = DISPLAY.create_pen(0, 0, 0)

# CGA PALETTE 1 (HIGH) - https://lospec.com/palette-list/cga-palette-1-high
LIGHTEST = DISPLAY.create_pen(156, 210, 126)
LIGHT = LIGHTEST
DARK = DISPLAY.create_pen(172, 109, 209)
DARKEST = DISPLAY.create_pen(53, 53, 53)

# Change your badge and QR details here!
COMPANY_NAME = "ANE 2025!!"
NAME = "Kabit"
BLURB1 = "Am Bnnny"
BLURB2 = "Not a fox"
BLURB3 = "#1 it/she bun"

QR_TEXT = "linktr.ee/kabit"

IMAGE_DIR = "images/120x120/"
IMAGES = os.listdir(IMAGE_DIR)
IMAGE_DURATION = 60

# Some constants we'll use for drawing
BORDER_SIZE = 4
PADDING = 10
COMPANY_HEIGHT = 40

def draw_badge():
    # draw border
    DISPLAY.set_pen(LIGHTEST)
    DISPLAY.clear()

    # draw background
    DISPLAY.set_pen(DARK)
    DISPLAY.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw company box
    DISPLAY.set_pen(DARKEST)
    DISPLAY.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), COMPANY_HEIGHT)

    # draw company text
    DISPLAY.set_pen(LIGHT)
    DISPLAY.set_font("bitmap6")
    DISPLAY.text(COMPANY_NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING, WIDTH, 3)

    # draw name text
    DISPLAY.set_pen(LIGHTEST)
    DISPLAY.set_font("bitmap8")
    DISPLAY.text(NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING + COMPANY_HEIGHT, WIDTH, 5)

    # draws the bullet points
    DISPLAY.set_pen(DARKEST)
    DISPLAY.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 105, 160, 2)
    DISPLAY.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 140, 160, 2)
    DISPLAY.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 175, 160, 2)

    # draws the blurb text (4 - 5 words on each line works best)
    DISPLAY.set_pen(LIGHTEST)
    DISPLAY.text(BLURB1, BORDER_SIZE + PADDING + 135 + PADDING, 105, 160, 2)
    DISPLAY.text(BLURB2, BORDER_SIZE + PADDING + 135 + PADDING, 140, 160, 2)
    DISPLAY.text(BLURB3, BORDER_SIZE + PADDING + 135 + PADDING, 175, 160, 2)


def show_photo(filename):
    j = jpegdec.JPEG(DISPLAY)

    # Open the JPEG file
    j.open_file(f"{IMAGE_DIR}/{filename}")

    # Draws a box around the image
    DISPLAY.set_pen(DARKEST)
    DISPLAY.rectangle(PADDING, HEIGHT - ((BORDER_SIZE * 2) + PADDING) - 120, 120 + (BORDER_SIZE * 2), 120 + (BORDER_SIZE * 2))

    # Decode the JPEG
    j.decode(BORDER_SIZE + PADDING, HEIGHT - (BORDER_SIZE + PADDING) - 120)

    # Draw QR button label
    DISPLAY.set_pen(LIGHTEST)
    DISPLAY.text("QR", 240, 215, 160, 2)


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    DISPLAY.set_pen(LIGHTEST)
    DISPLAY.rectangle(ox, oy, size, size)
    DISPLAY.set_pen(DARKEST)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                DISPLAY.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


def show_qr():
    DISPLAY.set_pen(DARK)
    DISPLAY.clear()

    code = qrcode.QRCode()
    code.set_text(QR_TEXT)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)

def main():
    buttons = ButtonHandler()

    # draw the badge for the first time
    badge_mode = "photo"
    image_gen = WrappedGeneratorTimer(IMAGES, IMAGE_DURATION)
    photo = image_gen.next()
    draw_badge()
    show_photo(photo)
    DISPLAY.update()

    while True:
        flags = buttons.get_flags()
        if "a" in flags and "c" in flags:
            break

        if buttons.get_flag("c"):
            if badge_mode == "photo":
                badge_mode = "qr"
                show_qr()
                DISPLAY.update()
            else:
                badge_mode = "photo"
                draw_badge()
                show_photo(photo)
                DISPLAY.update()
        
        if photo != image_gen.next() and badge_mode == "photo":
            photo = image_gen.next()
            show_photo(photo)
            DISPLAY.update()

        buttons.reset()
        time.sleep_ms(250)

if __name__ == "__main__":
    main()
