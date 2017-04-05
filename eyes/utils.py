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
    except error.Error as e:
        parser.error(e)

    return device
