#!/usr/bin/env python3

import os

class Mister():
    def __init__(self):
        self.sdroot = 'media/fat/games' # this is fairly consistent for the project
        return


    def mkdir(self, d):
        if not os.path.exists(d):
            return os.mkdir(d)
        return 