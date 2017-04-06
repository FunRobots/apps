# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

import sys
import logging
import argparse
from luma.core import cmdline, error

EYES_LCD_CONFIG_FILE = "eyes.conf"

def load_config(path_to_config):
    """
    Load device configuration from file path and return list with parsed lines.
    
    :param path: Location of configuration file.
    :type path: str
    :rtype: list
    """
    args = []
    with open(path_to_config, 'r') as fp:
        for line in fp.readlines():
            if line.strip() and not line.startswith("#"):
                args.append(line.replace("\n", ""))

    return args


def get_device():
    """
    Create device from command-line arguments and return it.
    """
    config = load_config(EYES_LCD_CONFIG_FILE)
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(config)

    # create device
    try:
        device = cmdline.create_device(args)
        #settings for LCD size 
        device.bounding_box = (0, 0, 127, 127)
        device.size = (128, 128)
        device.framebuffer.bounding_box = (0, 0, 127, 127)
    except error.Error as e:
        parser.error(e)

    return device


def convert_params_to_coord(angle, distane_from_center_percent, outer_radius):
    import math 
    
    angle_rad = math.radians(360 - angle)
    distance = distane_from_center_percent * outer_radius
    x = math.ceil(distance * math.cos(angle_rad))
    y = math.ceil(distance * math.sin(angle_rad))
    
    return x, y

def primitives(device, draw):
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = device.height - padding - 1
    # Move left to right keeping track of the current x position for drawing shapes.
    x = padding
    # Draw an ellipse.
    draw.ellipse((x, top, x + shape_width, bottom), outline="red", fill="black")
    x += shape_width + padding
    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, bottom), outline="blue", fill="black")
    x += shape_width + padding
    # Draw a triangle.
    draw.polygon([(x, bottom), (x + shape_width / 2, top), (x + shape_width, bottom)], outline="green", fill="black")
    x += shape_width + padding
    # Draw an X.
    draw.line((x, bottom, x + shape_width, top), fill="yellow")
    draw.line((x, top, x + shape_width, bottom), fill="yellow")
    x += shape_width + padding
    # Write two lines of text.
    size = draw.textsize('World!')
    x = device.width - padding - size[0]
    draw.rectangle((x, top + 4, x + size[0], top + size[1]), fill="black")
    draw.rectangle((x, top + 16, x + size[0], top + 16 + size[1]), fill="black")
    draw.text((device.width - padding - size[0], top + 4), 'Hello', fill="cyan")
    draw.text((device.width - padding - size[0], top + 16), 'World!', fill="purple")
    # Draw a rectangle of the same size of screen
    draw.rectangle(device.bounding_box, outline="white")