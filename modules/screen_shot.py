#!/usr/bin/env python
##########################################################
# screen_shot.py v4.0 by level6
# https://github.com/lleevveell66/HyperClock
##########################################################

"""
This module will wait for the 's' to be pressed, then take a snapshot
of the pygame surface and save it as a PNG into the snapshots/ directory.
"""

import os
import curses
from PIL import Image        # Requires Pillow: yum -y install python3-pillow / pip install Pillow

def save_screenshot(screen, filename):
    """
    Saves the screenshot to the specified file.
    """

    try:
        # Convert the Pygame Surface to a PIL Image
        mode = screen.get_bitsize()  # Get the color depth
        if mode == 8:
            my_format = "P"  # Paletted image format
        elif mode == 16:
            my_format = "RGB"
        elif mode == 24:
            my_format = "RGB"
        elif mode == 32:
            my_format = "RGBA"
        else:
            my_format = "RGB"

        image = Image.frombytes(my_format, screen.get_size(), screen.get_view(screen.get_rect()))
        image.save(filename, "PNG")
        print(f"Screenshot saved to {filename}")

    except Exception as error:
        print(f"Error saving screenshot: {error}")

key = stdscr.getch()

if key == 27:
    screenshot_filename = os.path.join("snapshots", f"screenshot_{pygame.time.get_ticks()}.png")
    save_screenshot(my_screen, screenshot_filename)
else:
    key_pressed = chr(key)
    debug_print("Key pressed: {key_pressed}")

stdscr.refresh()
