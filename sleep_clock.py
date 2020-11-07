#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# Changed by Sebastian Schmittner
# See LICENSE.rst for details.

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def demo(n, block_orientation):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=2)

    device.contrast(0)
    while True:
        now = time.localtime()

        with canvas(device) as draw:
            text(draw, (0,0), "{:02}:{:02}".format(now.tm_hour, now.tm_min), fill="white", font=proportional(CP437_FONT))

        if now.tm_hour < 6 or now.tm_hour > 22:
            device.hide()
            device.clear()
            sleep(60*(60 - now.tm_min))
            device.show()




if __name__ == "__main__":
    try:
        demo(4, 'vertical')
    except KeyboardInterrupt:
        pass
