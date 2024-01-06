#!/usr/bin/env python3

import os
from lib.config import Config
from lib.archive import Archive
from lib.client_local import ClientDIR

class Mister():
    def __init__(self, sdroot="media/fat/games", system=None):
        print("MisterFPGA support started")
        self.sdroot = sdroot
        self.config = Config()
        self.sysfile = os.path.join(self.config.config_dir_systems,'%s.yaml' % system)
        self.sysconfig = self.config.read_config_system(self.sysfile)
        self.config.read_config_main()
        self.mainconfig = self.config.config_main
        self.mister_core = self.sysconfig['mister_core']
        if self.mister_core == "" or self.mister_core == "NONE":
            print("No core defined in system config")
            return
        self.mountpoint = os.path.join(self.mainconfig['mister_mount'], self.sdroot, self.sysconfig['mister_core'])
        self.mkdir(self.mountpoint)

    def mkdir(self, d):
        if not os.path.exists(d):
            return os.mkdir(d)
        return 

    def vars(self, data=None):
        return {}

    def collection(self, data=None):
        return

    def entry(self, data=None):
        self.dataset = data
        return

    def dump(self, system=None):
        client = ClientDIR(self.mountpoint)
        a = Archive()
        a.extract(self.dataset, client)
        return