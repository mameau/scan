#!/usr/bin/env python3

import os
import re
from lib.config import Config

class Generic():
    def __init__(self, mode='file', system=None, output=None):
        self.config = Config()
        self.mode = mode
        self.sysfile = os.path.join(self.config.config_dir_systems,'%s.yaml' % system)
        if output is not None:
            self.sysconfig = self.config.read_config_system(self.sysfile, output.vars())
        else:
            self.sysconfig = self.config.read_config_system(self.sysfile)
        return

    def create_list(self, p, e=[]):
        filelist = {}
        e = [x.strip(' ') for x in e]
        for root, dirs, files in os.walk(os.path.expanduser(p)):
            if self.mode == 'dir':
                for dirname in dirs:
                    abspath = os.path.join(root,dirname)
                    name = dirname
                    if os.path.exists(abspath):
                        filelist[name] = abspath
            elif self.mode == 'file':
                for filename in files:
                    abspath = os.path.join(root,filename)
                    ext = os.path.splitext(abspath)[-1]
                    try:
                        ext = ext.replace('.','')
                    except:
                        pass
                    if ext in e:
                        name = '. '.join(os.path.splitext(filename)[:-1])
                        if os.path.exists(abspath):
                            filelist[name] = abspath
            elif self.mode == 'file-parent':
                for filename in files:
                    abspath = os.path.join(root,filename)
                    ext = os.path.splitext(abspath)[-1]
                    try:
                        ext = ext.replace('.','')
                    except:
                        pass
                    if ext in e:
                        name = os.path.basename(root)
                        if os.path.exists(abspath):
                            filelist[name] = abspath
        return filelist

    def generate_name_from_file(self, name):
        print(os.path.splitext(name))
        return '. '.join(os.path.splitext(name)[:-1])

    def populate_cache(self, filelist={}, year="????", manufacturer="Unspecified", driver_status="Unknown"):

        for filename in filelist:
            basename = os.path.basename(filename)
            game_name = filename
            game_ext = os.path.splitext(basename)[-1]
            description = filename
            year = year
            manufacturer = manufacturer
            driver_status = "Unknown"
            display_orientation = 0
            players = 1

            self.mindata[game_name] = {
                'name' : description,
                'description' : description,
                'name_rom' : "%s" % game_name,
                'name_pretty' : "%s (%s).%s" % (description, game_name, game_ext),
                'name_sl'     : game_name,
                'rom_abspath' : filelist[filename],
                'year' : year,
                'manufacturer' : manufacturer,
                'driver_status' : driver_status,
                'display_orientation' : display_orientation,
                'players' : players,
            }

    def scan(self):
        self.mindata = {}
        dataset = self.create_list(self.sysconfig['rom_dir'], self.sysconfig['extensions'].split(','))
        self.populate_cache(dataset)
        return self.mindata