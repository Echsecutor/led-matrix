#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# Changed by Sebastian Schmittner
# See LICENSE.rst for details.

import time

from luma.led_matrix.device import max7219
from luma.core.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

from PIL import Image
from io import BytesIO
import logging
import requests
import os


def vertical_scroll(device, msg):
    logging.debug("vertical scroll '{}'".format(msg))
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.2)

    
def horizontal_scroll_msg(device, msg):
    logging.debug("horizontal scroll '{}'".format(msg))
    virtual = viewport(device, width=device.width, height=3*8)
    with canvas(virtual) as draw:
        text(draw, (0, 8), msg, fill="white", font=proportional(CP437_FONT))
    horizontal_scroll(device, virtual)


def horizontal_sroll(device, virtual):
    for i in range(virtual.height - device.height):
        virtual.set_position((0, i))
        time.sleep(0.2)


def display_img_from_file(device, img_dir, file_name):
    img_path = os.path.join(img_dir, file_name)
    img = Image.open(img_path)
    logging.debug("image: {}".format(img_path))
    display_img(device, img)


def display_img_from_url(device, url):
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))
    logging.debug("img loaded from {}".format(url))
    display_img(device, img)


def display_img(device, img):
    img_width, img_height = img.size
    logging.debug("original image size: {} = ({}, {})".format(img.size, img_width, img_height))
    dev_width, dev_height = device.size
    scale = float(dev_width) / float(img_width)
    logging.debug("scale: {}".format(scale))
    
    virtual = viewport(device, width=device.width, height=int(img_height*scale))
    img = img.resize(virtual.size)
    alpha_band = Image.new(mode="1", size=img.size)
    alpha_band.putdata([0 for x in range(img.size[0]*img.size[1])])
    img.putalpha(alpha_band)
    img = img.convert(mode="1")
    logging.debug("image mode: {}, device mode: {}".format(img.mode,
                                                           device.mode))
    logging.debug("image size: {}, device size: {}".format(img.size,
                                                           device.size))

    virtual.display(img)
    horizontal_sroll(device, virtual)
    time.sleep(2)

    
def show_weather(device):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=cologne&APPID=ea53b55b32be6dcb7f97bc6497d398a1&units=metric').json()
    logging.debug(r)
    msg = "{:.1f}°C {}".format(r["main"]["temp"], r["weather"][0]["main"])
    icon_url = "http://openweathermap.org/img/w/{}.png".format(r["weather"][0]["icon"])
    display_img_from_url(device, icon_url)
    vertical_scroll(device, msg)
    
    
def show_greetings(device):
    now = time.localtime()
    if now.tm_hour < 10:
        msg = "Guten Morgen! :-)"
    elif now.tm_hour < 17:
        msg = "Hallo! :)"
    elif now.tm_hour < 20:
        msg = "Guten Abend!"
    else:
        msg = "Gute Nacht! Zzz"

    vertical_scroll(device, msg)

    
def show_date(device):
    now = time.localtime()
    msg = "{:02}.{:02}.".format(now.tm_mday, now.tm_mon)
    horizontal_scroll_msg(device, msg)


def show_time(device):
    now = time.localtime()
    msg = "{:02}:{:02}".format(now.tm_hour, now.tm_min)
    horizontal_scroll_msg(device, msg)

            
def loop(device, display_actions):
    while True:
        for action in display_actions:
            try:
                action(device)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(e.message)
            time.sleep(1)
        
                
def main():
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, mode="1")
    device.contrast(0)

    log_config = {"level": "INFO"}
    logging.basicConfig(**log_config)
    
    loop(device, [show_greetings, show_weather, show_time, show_date])
    #loop(device, [show_weather])


if __name__ == "__main__":
    import argparse

    logger_cfg = {
        "level":logging.INFO,
        "format":"%(asctime)s %(funcName)s (%(lineno)d) [%(levelname)s]:    %(message)s"
    }
    parser = argparse.ArgumentParser(description="Display Messages on an Raspberry Pi connected LED matrix display(4 x 8 x 8)")
    parser.add_argument(
        "-l",
        "--log",
        help="Set the log level. Default: INFO.",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO")

    args = parser.parse_args()

    logger_cfg["level"] = getattr(logging, args.log)
    logging.basicConfig(**logger_cfg)
                            
    try:
        main()
    except KeyboardInterrupt:
        pass
