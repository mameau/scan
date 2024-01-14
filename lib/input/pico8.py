#!/usr/bin/env python3

import os
import re

from lib.config import Config
from lib.input.generic import Generic

config = Config()


class PICO8():
    def __init__(self):
        self.system = 'pico8'
        self.generic = Generic(system=self.system)
        self.sysfile = os.path.join(config.config_dir_systems,'%s.yaml' % self.system)
        self.sysconfig = config.read_config_system(self.sysfile)
        return

    def scan(self):
        self.generic.mindata = {}
        filelist = self.generic.create_list(self.sysconfig['rom_dir'], ['zip'])
        filelist.update({'splore':"splore"})
        self.generic.populate_cache(filelist=filelist, manufacturer="lexaloffle", year="20??", driver_status="Good")
        return self.generic.mindata
