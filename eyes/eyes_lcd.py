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
import time
from itertools import izip_longest #use zip_longest for Python3 
from operator import itemgetter
from luma.core.serial import spi
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.lcd.device import st7735 

from utils import get_device


class Eyes(object):
    def __init__(self, width, height, background_color, eye_radius, eye_color, pupil_radius, pupil_color):
        #LCD base settings
        self._w = width
        self._h = height
        self._color = background_color
        self._eye_radius = eye_radius
        self._eye_color = eye_color
        
        #Eyes base settings 
        self._x_pos = self._w / 2.0
        self._y_pos = self._h / 2.0
        # self.bound_box =  (0, 0, width, height)  #seems needless TODO: delete at next commit
        # self.outer_radius = (self.bound_box[2] - self.bound_box[0]) / 2   #seems needless TODO: delete at next commit
        self._pupil_radius = pupil_radius 
        self._pupil_orbit_radius = self._eye_radius - self._pupil_radius
        self._pupil_color = pupil_color
        
        #speed settings 
        self._x_speed = 5
        self._y_speed = 5

    def update_pos(self, x_step = None, y_step = None):
        if x_step is None:
            x_step = self._x_speed
        if y_step is None:
            y_step = self._y_speed
        
        if self._x_pos + self._pupil_radius > self._w:
            self._x_speed = -abs(x_step)
        elif self._x_pos - self._pupil_radius < 0.0:
            self._x_speed = abs(x_step)

        if self._y_pos + self._pupil_radius > self._h:
            self._y_speed = -abs(y_step)
        elif self._y_pos - self._pupil_radius < 0.0:
            self._y_speed = abs(y_step)

        self._x_pos += self._x_speed
        self._y_pos += self._y_speed
         
    def draw(self, canvas):
        #draw eye
        canvas.ellipse((0,self._eye_radius, 0, self._eye_radius),
                     fill=self._eye_color,
                     outline=self._eye_color)        
        #draw pupil
        canvas.ellipse((self._x_pos - self._pupil_radius, 
                      self._y_pos - self._pupil_radius,
                      self._x_pos + self._pupil_radius, 
                      self._y_pos + self._pupil_radius),
                     fill=self._pupil_color,
                     outline=self._pupil_color)

    #eyes control methods 
    def get_eyes_position(self):
        return (self._x_pos, self._y_pos)
    
    def set_eyes_position(self, x, y, canvas):
        #define steps to set eyes into new position (x,y)
        def get_path_to_point(self, goal, self_pos, speed):
            path = []
            move = (goal - self_pos) / speed
            steps_number = int(math.copysign(move, speed))
            step_speed = int(math.copysign(speed, move))
            [path.append(step_speed) for step in range(1, steps_number)]
            return path
        
        x_path = get_path_to_point(x, self._x_pos,  self._x_speed)
        y_path = get_path_to_point(y, self._y_pos,  self._y_speed)
        
        #for each step: update position, draw eyes 
        for x_step, y_step in izip_longest(x_path, y_path, fillvalue=0):
            self.update_pos(x_step, y_step)
            self.draw(canvas) 


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
    device = get_device()
    eyes = Eyes(width=128, 
        height=128, 
        background_color='#14F6FA',
        eye_radius=46, 
        eye_color='#14F6FA', 
        pupil_radius=10, 
        pupil_color='#14F6FA')

    frame_count = 0
    fps = ""
    regulator = framerate_regulator(fps=10)

    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            frame_count += 1
            with canvas(device) as draw:
                # draw_eye(draw, random.randint(0, 360), random.uniform(0, 1))
                eyes.draw(draw)
                time.sleep(5)
                eyes.set_eyes_position(120, 120, draw)

            if frame_count % 20 == 0:
                fps = "FPS: {0:0.3f}".format(regulator.effective_FPS())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
