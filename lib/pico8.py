#!/usr/bin/env python3

import os
import re

import lib.scanner as scanner
import lib.filelist as filelist
import lib.config as config

class PICO8():
    def init(self):
        return

    def create_list(self, d):
        for root, dirs, files in os.walk(os.path.expanduser(d)):
            for filename in files:
                abs_path = os.path.join(root, filename)
                self.populate_cache(filename)
        return

    def generate_name_from_file(self, name):
        return os.path.splitext(name)[0]

    def populate_cache(self, game_name):

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


    def scan(self, sysconfig=None):
        self.mindata = {}
        self.populate_cache("splore")
        self.create_list(sysconfig['rom_dir'])
        return self.mindata
