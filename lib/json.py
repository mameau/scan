#!/usr/bin/env python3

import os
import json
import re

import lib.logger as logger
import lib.config as config

class JSON():
    def __init__(self):
        self.jsonconfig_data = {}
        pass

    def collection(self, data=None):
        self.jsonconfig_data['collection'] = data
        return

    def entry(self, data=None):
        self.jsonconfig_data['entries'] = data
        return

    def dump(self, system=None):
        logger.Logger()._log("Writing %d items to cache file" % len(self.jsonconfig_data))
        if self.jsonconfig_data is not None and len(self.jsonconfig_data) > 0: 
            outfile = os.path.join(config.Config().config_dir,'_cache','%s.json' % system)
            logger.Logger()._log("Writing %d items to cache file %s" % (len(self.jsonconfig_data), outfile))
            with open(outfile,'w') as f:
                json.dump(self.jsonconfig_data, f)
        else:
            logger.Logger()._log("Not writing cache file, no entries to write")
