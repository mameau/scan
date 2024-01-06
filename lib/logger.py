#!/usr/bin/env python3

import os
import time

class Logger():
    def __init__(self):
        self.debug = False
        self.startval = 0
        self.runstartval = 0
        pass

    def _log(self,s):
        print(s)

    def timestr(self, dt):
        # units
        self._log(" Time taken: %fs" % (dt / 1000000000))

    def getnow(self):
        return time.time_ns()

    def start(self):
        self.startval = self.getnow()

    def end(self):
        self.timestr(self.getnow() - self.startval)

    def runstart(self):
        self.runstartval = self.getnow()

    def runend(self):
        self.timestr(self.getnow() - self.runstartval)

    def summary(self):
        self._log("Summary")