#!/usr/bin/env python3

import os
import yaml
import re

from lib.logger import Logger
from lib.config import Config

config = Config()
logger = Logger()

class YAML():
    def __init__(self, extension="yaml"):
        print("YAML support started")
        self.data = {}
        self.extension = extension
        pass

    def collection(self, data=None):
        self.data['system'] = data
        return

    def entry(self, data=None):
        self.data['entries'] = data
        return

    def vars(self):
        return {}

    def dump(self, system=None):
        if self.data is not None and len(self.data) > 0: 
            outfile = os.path.join(config.config_dir_cache,'%s.%s' % (system, self.extension))
            logger._log("Writing %d items to cache file %s" % (len(self.data), outfile))

            with open(outfile,'w') as f:
                yaml.dump(self.data, f)
        else:
            logger._log("Not writing cache file, no entries to write")
