#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Rotating 3D box wireframe & color dithering.

Adapted from:
http://codentronix.com/2011/05/12/rotating-3d-cube-using-python-and-pygame/
"""

import sys
import math
import random 
from ppretty import ppretty
from operator import itemgetter
from luma.core.serial import spi
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.lcd.device import st7735 

from utils import get_device


def convert_params_to_coord(angle, distane_from_center_percent, outer_radius):
    import math 
    
    angle_rad = math.radians(360 - angle)
    distance = distane_from_center_percent * outer_radius
    x = math.ceil(distance * math.cos(angle_rad))
    y = math.ceil(distance * math.sin(angle_rad))
    
    return x, y

def draw_eye(draw, angle, distane_from_center_percent):
    #settings 
    bound_box = (1, 1, 127, 127)
    center_coords = (64, 64)
    outer_radius = (bound_box[2] - bound_box[0]) / 2
    pr = 20  #pupil radius 
    pupil_radius = outer_radius - pr
    
    #calc x, y shift from center
    x, y = convert_params_to_coord(angle, distane_from_center_percent, pupil_radius)  
     
    x0 = center_coords[0] + x - pr
    y0 = center_coords[1] + y - pr
    x1 = center_coords[0] + x + pr
    y1 = center_coords[1] + y + pr
    
    
    #eye outer border
    draw.ellipse((3, 3, 125, 125), '#14F6FA', '#14F6FA')
    
    #eye pupil 
    eye_tuple = (x0, y0, x1, y1)
    draw.ellipse(eye_tuple, 'black', 'black') 

    
    return draw


def main(num_iterations=sys.maxsize):
    colors = ["red", "orange", "yellow", "green", "blue", "magenta"]

    frame_count = 0
    fps = ""
    regulator = framerate_regulator(fps=10)

    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            frame_count += 1
            with canvas(device) as draw:
                draw_eye(draw, random.randint(0, 360), random.uniform(0, 1))

            if frame_count % 20 == 0:
                fps = "FPS: {0:0.3f}".format(regulator.effective_FPS())


if __name__ == "__main__":
    try:
        device = get_device()
        device.bounding_box = (0, 0, 127, 127)
        device.size = (128, 128)
        device.framebuffer.bounding_box = (0, 0, 127, 127)
        print(ppretty(device, indent='  ', depth=5, width=120, seq_length=10, show_protected=False, show_private=True,
                show_static=True, show_properties=True, show_address=True))
        main()
    except KeyboardInterrupt:
        pass
