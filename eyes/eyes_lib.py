# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

import sys
from luma.core import cmdline, error
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator


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


def create_canvas(device):
    return canvas(device)


def set_display_frame_rate(fps):
    return framerate_regulator(fps)


def convert_params_to_coord(angle, distance_from_center_percent, outer_radius):
    import math

    if angle is None:
        angle = 0
    if distance_from_center_percent is None:
        distance_from_center_percent = 0
    
    angle_rad = math.radians(360 - angle)
    distance = distance_from_center_percent * outer_radius
    x = math.ceil(distance * math.cos(angle_rad))
    y = math.ceil(distance * math.sin(angle_rad))
    
    return x, y


def draw_eye(eyes_canvas, emotion, x0, y0, x1, y1, fill='#14F6FA', outline='#14F6FA'):
    # # default settings:
    # x0 = 0
    # y0 = 0
    # x1 = 128
    # y1 = 128
    frame_rate_regulator = set_display_frame_rate(fps=30)  # framerate change speed
    with frame_rate_regulator:
        # eye outer border
        eyes_canvas.ellipse((x0, y0, x1, y1), fill=fill, outline=outline)

