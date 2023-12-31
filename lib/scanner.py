#!/usr/bin/env python3

import os
import json
import re

import lib.logger as logger
import lib.config as config

class Scanner():
    def __init__(self):
        pass

    def _cache(self, data, system):
        logger.Logger()._log("Writing %d items to cache file" % len(data))
        if len(data) > 0: 
            outfile = os.path.join(config.Config().config_dir,'_cache','%s.json' % system)
            logger.Logger()._log("Writing %d items to cache file %s" % (len(data), outfile))
            with open(outfile,'w') as f:
                json.dump(data, f)
        else:
            logger.Logger()._log("Not writing cache file, no entries to write")
