#!/usr/bin/env python3

import os
import json
import re

import lib.logger as logger
from lib.config import Config

config = Config()

class JSON():
    def __init__(self):
        print("JSON support started")
        self.jsonconfig_data = {}
        pass

    def collection(self, data=None):
        self.jsonconfig_data['system'] = data
        return

    def entry(self, data=None):
        self.jsonconfig_data['entries'] = data
        return

    def vars(self):
        return {}

    def dump(self, system=None):
        if self.jsonconfig_data is not None and len(self.jsonconfig_data) > 0: 
            outfile = os.path.join(config.config_dir_cache,'%s.json' % system)
            logger.Logger()._log("Writing %d items to cache file %s" % (len(self.jsonconfig_data), outfile))
            with open(outfile,'w') as f:
                json.dump(self.jsonconfig_data, f)
        else:
            logger.Logger()._log("Not writing cache file, no entries to write")
