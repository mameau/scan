#!/usr/bin/env python3

import os
import re

from lib.config import Config
from lib.generic import Generic


class PICO8():
    def __init__(self):
        config = Config()
        generic = Generic()

        self.system = 'pico8'
        self.sysfile = os.path.join(config.config_dir_systems,'%s.yaml' % system)
        self.sysconfig = config.read_config_system(self.sysfile, output.vars())
        return

    def vars(self):
        game_name = os.path.splitext(game_name)[0]
        game_ext = os.path.splitext(game_name)[1]
        description = self.generate_name_from_file(game_name)
        year = "20??"
        manufacturer = "lexaloffle"
        driver_status = "good"
        display_orientation = 0
        players = 1

        self.mindata[game_name] = {
            'name' : description,
            'description' : description,
            'name_rom' : "%s" % game_name,
            'name_pretty' : "%s (%s).%s" % (description, game_name, game_ext),
            'name_sl'     : game_name,
            'rom_abspath' : game_name,
            'year' : year,
            'manufacturer' : manufacturer,
            'driver_status' : driver_status,
            'display_orientation' : display_orientation,
            'players' : players,
        }        

    def scan(self):
        self.mindata = {}
        self.populate_cache("splore")
        self.create_list(sysconfig['rom_dir'])
        return self.mindata
