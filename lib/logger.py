#!/usr/bin/env python3

import os
import time

class Logger():
    def __init__(self):
        self.debug = False
        pass

    def _log(self,s):
        print(s)

    def timestr(self, dt):
        # units
        self._log(" Time taken: %fs" % (dt / 1000000000))

    def getnow(self):
        return time.time_ns()