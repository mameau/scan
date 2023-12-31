#!/usr/bin/env python3

import os
import yaml
import lib.config as config

class Pegasus():
    def __init__(self):
        self.pegasus_config_dir = os.path.expanduser('~/.config/pegasus-frontend')
        self.pegasus_config_gamedirs = os.path.join(self.pegasus_config_dir,'game_dirs.txt')
        self.pegasus_config_data = {}
        return

    def collection(self, data=None):
        self.pegasus_config_data['collection'] = data['display_name']
        self.pegasus_config_data['extension'] = data['extensions']
        self.pegasus_config_data['launch'] = data['cmd']
        self.pegasus_config_data['entries'] = []
        return

    def entry(self, data=None):
        for entry in data:
            entry = data[entry]
            game_data = {}
            game_data['game'] = entry['name']
            game_data['file'] = entry['rom_abspath']
            game_data['developer'] = entry['manufacturer']
            game_data['year'] = entry['year']
            game_data['genre'] = "Unspecified"
            game_data['players'] = entry['players']
            game_data['description'] = entry['description']
            game_data['rating'] = "Unspecified"
            self.pegasus_config_data['entries'].append(game_data)
        return

    def dump(self, system=None):

        # fake yaml to satisfy pegasus
        for k in self.pegasus_config_data:
            if k != 'entries':
                print(f"{k}: {self.pegasus_config_data[k]}")

        print("")
        for e in self.pegasus_config_data['entries']:
            for g in e:
                print(f"{g}: {e[g]}")
            print("")
        return