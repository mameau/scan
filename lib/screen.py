#!/usr/bin/env python3

import os

import lib.logger as logger
import lib.config as config

class Screen():
    def __init__(self):
        print("Screen support started")
        self.data = {}
        pass

    def collection(self, data=None):
        self.data['collection'] = data
        return

    def entry(self, data=None):
        self.data['entries'] = data
        return

    def vars(self):
        return {}

    def dump(self, system=None):
        print(self.data)
        return
