#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Text Input LED Matrix Display Script
# Based on LED matrix project by Sebastian Schmittner

import time
import logging
import argparse

from luma.led_matrix.device import max7219
from luma.core.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT


def vertical_scroll(device, msg):
    """Display text with vertical scrolling animation"""
    logging.debug("Vertical scroll: '{}'".format(msg))
    show_message(device, msg, fill="white",
                 font=proportional(LCD_FONT), scroll_delay=0.1)


def horizontal_scroll(device, virtual):
    """Perform horizontal scrolling animation"""
    for i in range(virtual.height - device.height):
        virtual.set_position((0, i))
        time.sleep(0.2)


def horizontal_scroll_msg(device, msg):
    """Display text with horizontal scrolling animation"""
    logging.debug("Horizontal scroll: '{}'".format(msg))
    virtual = viewport(device, width=device.width, height=3*8)
    with canvas(virtual) as draw:
        text(draw, (0, 8), msg, fill="white", font=proportional(CP437_FONT))
    horizontal_scroll(device, virtual)


def static_display(device, msg, duration=5):
    """Display text statically for a specified duration"""
    logging.debug("Static display: '{}'".format(msg))
    with canvas(device) as draw:
        text(draw, (0, 0), msg, fill="white", font=proportional(CP437_FONT))
    time.sleep(duration)


def display_text(device, text_input, display_mode="vertical"):
    """Display text using the specified mode"""
    if display_mode == "vertical":
        vertical_scroll(device, text_input)
    elif display_mode == "horizontal":
        horizontal_scroll_msg(device, text_input)
    elif display_mode == "static":
        static_display(device, text_input)
    else:
        logging.warning(
            "Unknown display mode '{}', using vertical scroll".format(display_mode))
        vertical_scroll(device, text_input)


def get_user_input():
    """Get text input from user with options"""
    print("\n=== LED Matrix Text Display ===")
    print("Enter text to display on the LED matrix.")
    print("Available display modes:")
    print("  1. Vertical scroll (default)")
    print("  2. Horizontal scroll")
    print("  3. Static display")
    print("  4. Quit")

    while True:
        text_input = input("\nEnter your text: ").strip()

        if not text_input:
            print("Please enter some text.")
            continue

        if text_input.lower() in ['quit', 'exit', 'q']:
            return None, None

        print("\nSelect display mode:")
        print("1. Vertical scroll")
        print("2. Horizontal scroll")
        print("3. Static display")

        mode_choice = input("Enter choice (1-3, default=1): ").strip()

        mode_map = {
            '1': 'vertical',
            '2': 'horizontal',
            '3': 'static',
            '': 'vertical'  # default
        }

        if mode_choice in mode_map:
            return text_input, mode_map[mode_choice]
        else:
            print("Invalid choice, using vertical scroll.")
            return text_input, 'vertical'


def main():
    """Main function to setup device and handle user interaction"""
    # Create matrix device with same configuration as existing scripts
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-
                     90, rotate=2, mode="1")
    device.contrast(0)

    print("LED Matrix Text Display initialized.")
    print("Hardware: 4x8x8 LED matrices (32x8 total resolution)")

    try:
        while True:
            text_input, display_mode = get_user_input()

            if text_input is None:  # User wants to quit
                print("Goodbye!")
                break

            print("Displaying: '{}' in {} mode".format(text_input, display_mode))
            display_text(device, text_input, display_mode)

            # Ask if user wants to continue
            continue_choice = input(
                "\nDisplay another message? (y/n, default=y): ").strip().lower()
            if continue_choice in ['n', 'no']:
                print("Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")
    finally:
        device.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interactive text display for Raspberry Pi LED matrix (4 x 8 x 8)"
    )
    parser.add_argument(
        "-l",
        "--log",
        help="Set the log level. Default: INFO.",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO"
    )
    parser.add_argument(
        "-t",
        "--text",
        help="Text to display (if not provided, will prompt interactively)"
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Display mode",
        choices=["vertical", "horizontal", "static"],
        default="vertical"
    )

    args = parser.parse_args()

    # Configure logging
    logger_cfg = {
        "level": getattr(logging, args.log),
        "format": "%(asctime)s %(funcName)s (%(lineno)d) [%(levelname)s]: %(message)s"
    }
    logging.basicConfig(**logger_cfg)

    # If text provided via command line, display it once and exit
    if args.text:
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=4,
                         block_orientation=-90, rotate=2, mode="1")
        device.contrast(0)

        print("Displaying: '{}' in {} mode".format(args.text, args.mode))
        display_text(device, args.text, args.mode)
        device.clear()
    else:
        # Interactive mode
        main()
