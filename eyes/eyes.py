#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 FunRobots Lab
# See LICENSE.rst for details.

"""
Candybot eyes module 

"""

import math
from itertools import izip_longest #use zip_longest for Python3
from eyes_lib import get_device, convert_params_to_coord, draw_eye, \
    set_display_frame_rate, create_canvas


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

        #device settings
        # self.device = get_device()
        # self.canvas = create_canvas(self.device)  # try to keep canvas outside Eyes (in main node script) !!!


    def set_eyes_position(self, x_step = None, y_step = None):
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


    #eyes control methods
    def get_eyes_position(self):
        return (self._x_pos, self._y_pos)


    def set_path_to_move_eyes(self, x, y):
        '''
            Calculate a path to set a position for eyes to move.
        '''

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

        return izip_longest(x_path, y_path, fillvalue=0)


    def set_emotion(self, emotion=None):
        if emotion is None:
            self.emotion = 'happy'
        self.emotion = emotion


    def get_emotion(self):
        return self.emotion



    def move_eyes(self, canvas, angle=None, distance_from_center_percent=None):

        # set default position
        if canvas is None:
            raise Exception('Error: canvas is None')
        if angle is None:
            angle = 0
        if distance_from_center_percent is None:
            distance_from_center_percent = 0

        # convert params to coords
        x, y = convert_params_to_coord(angle, distance_from_center_percent,
                                       self._eye_radius)

        #get path to move eyes
        path = self.set_path_to_move_eyes(self, x, y)

        # move eyes
        for x_step, y_step in path:
            # update eyes position
            self.set_eyes_position(x_step, y_step)

            # clear old pupil position - it seems unnecessary - TEST!!!
            # draw_eye(canvas,
            #          self.emotion,
            #          self._x_pos - self._pupil_radius,
            #          self._y_pos - self._pupil_radius,
            #          self._x_pos + self._pupil_radius,
            #          self._y_pos + self._pupil_radius,
            #          fill=self._pupil_color,
            #          outline=self._pupil_color)
            #

            # draw eye
            draw_eye(canvas = canvas,
                     emotion = self.emotion,
                     x0 = 0,
                     y0 = 0,
                     x1 = self._eye_radius,
                     y1 = self._eye_radius,
                     fill=self._eye_color,
                     outline=self._eye_color)

            # draw pupil
            draw_eye(canvas = canvas,
                     emotion = self.emotion,
                     x0 = self._x_pos - self._pupil_radius,
                     y0 = self._y_pos - self._pupil_radius,
                     x1 = self._x_pos + self._pupil_radius,
                     y1 = self._y_pos + self._pupil_radius,
                     fill=self._pupil_color,
                     outline=self._pupil_color)



def main():

    eyes = Eyes(width=128, 
        height=128, 
        background_color='#14F6FA',
        eye_radius=46, 
        eye_color='#14F6FA', 
        pupil_radius=10, 
        pupil_color='#14F6FA')

    # display settings
    device = get_device()
    canvas = create_canvas(device)
    frame_rate_regulator = set_display_frame_rate(fps=30)  # framerate change speed



    with frame_rate_regulator:
        # 30 fps expected
        with canvas:
            while True:

                # some subscribers code here
                angle = None
                distance_from_center_percent = None
                emotion = None

                # check params
                if angle is None & distance_from_center_percent is None:
                    # set default params to draw eyes in center position
                    eyes.move_eyes()

                # main instructions for eyes
                else:
                    # set eyes working mode
                    eyes.set_emotion(emotion)
                    eyes.move_eyes(canvas, angle, distance_from_center_percent)

                    # additional code here (i.e. publish eyes state)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
