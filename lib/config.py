#!/usr/bin/env python3

import os
import re
import glob
import yaml
import lib.logger as logger

class Config():
    def __init__(self):
        self.config_dir = os.path.expanduser('~/.scan')
        self.config_file = os.path.join(self.config_dir,'scan.yaml')
        self.config_example_system = os.path.join(self.config_dir,'yaml','system.yaml.example')
        self.inline_vars = {}
        self.config_generic = {}
        self.config_main = {}
        self.config_system = {}
        self.emulator = {}
        self.setup = {}
        self.read_config_main()
        return

    def __readconfig(self, config):
        """ read the ini into a dict object """
        self.confdict = {}
        if os.path.exists(config):
            with open(config, 'r') as file:
                self.confdict = yaml.safe_load(file)
        return self.confdict

    def read_config_main(self):        
        self.config_main = (self.__readconfig(self.config_file))

    def read_config_system(self, config):
        if not os.path.exists(config):  
            return

        self.config_system = (self.__readconfig(config))

        inline_vars = {
            'SYSTEM_NAME':self.config_system['name'],
            'GAME_EXEC':self.config_system['exec'],
            'ROM_EXT':self.config_system['extension'],
            'ROM_DIR':self.config_system['rom_dir'],
            }

        # read it a second time so we use any inline vars
        self.config_system = (self.__readconfig(config))

        # update dict from main_config vars
        for k in self.config_system:
            v = self.config_system[k]
            if v is not None:
                v = v.split("/")
            else:
                v = []
            z = []

            # this is shit, should be able to inline update the dict
            for i in v:
                # main config
                if i.lower() in self.config_main.keys():
                    z.append(self.config_main[i.lower()])
            if len(z) > 0:
                self.config_system[k] = '/'.join(z)
            else:
                self.config_system[k] = '/'.join(v)


            for i in v:
                # systems config
                if i.upper() in inline_vars.keys():
                    z.append(inline_vars[i])
            if len(z) > 0:
                self.config_system[k] = '/'.join(z)
            else:
                self.config_system[k] = '/'.join(v)

        return self.config_system

    def __readgenericconfig(self, config):
        """ read the ini into a dict object """
        self.confdict = {}
        if os.path.exists(config):
            #logger.Logger()._log("Reading config %s" % config)
            with open(config, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if not re.match('(#| )',line[0]):
                        match = re.match('^([a-z_]+)[\s]+(.*)$', line)
                        if match is not None:
                            k = match.group(1)
                            v = self.expand_user(match.group(2))
                            self.confdict[k] = self.__process_vars(v)
        return self.confdict

    def read_config_generic(self, config):
        self.config_generic.update(self.__readgenericconfig(config))
        return self.config_generic

    def get_current_system(self, index):
        self.current_system = self.emulator[index].copy()

    def get_systems(self):
        cntr = 0
        for sysconfig in glob.iglob(os.path.join(self.config_dir,'cfg','*.yaml')):
            sysname = os.path.splitext(os.path.basename(sysconfig))[0]
            if os.path.exists(os.path.join(self.config_dir,"_cache","%s.json" % sysname)):
                self.emulator[cntr] = self.read_config_system(sysconfig).copy()
                cntr += 1
            else:
                logger.Logger()._log("Skipping %s, no cache file found" % sysname)
        return self.emulator

    def process_launch_var(self, item):

        # launch opts dict, need selected
        launch_opts = {
                'ROM_NAME'  : item['name'],
                }
        
        ### build launch
        cmd = self.current_system['cmd']
        for key in launch_opts.keys():
            cmd = cmd.replace(key,launch_opts[key])
        print(cmd)
        return cmd

    def expand_user(self,s):
        return os.path.expanduser(s)

    def __process_vars(self, v):
        for key in self.inline_vars.keys():
                v = v.replace(key,self.inline_vars[key])
        return v
