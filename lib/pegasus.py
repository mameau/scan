#!/usr/bin/env python3

import os
import yaml
from lib.config import Config

class Pegasus():
    def __init__(self):
        print("Pegasus Frontend support started")
        self.config = Config()
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

    def vars(self):
        return {
            'ROM_EXT':'{file.ext}',
            'ROM_DIR':'{file.dir}',
            'ROM_NAME':'{file.name}',
            'ROM_BASENAME':'{file.basename}',
            'ROM_EXT':'{file.ext}',
            'ROM_PATH':'{file.path}',
            'ROM_URI':'{file.uri}',
            }


    def dump(self, system=None):

        outfile = os.path.join(self.config.config_dir_cache,'%s.metadata.pegasus.txt' % system)

        with open(outfile, 'w') as f:
            # fake yaml/text hybrid to satisfy pegasus
            for k in self.pegasus_config_data:
                if k != 'entries':
                    f.write(f"{k}: {self.pegasus_config_data[k]}\n")

            f.write("\n")
            for e in self.pegasus_config_data['entries']:
                for g in e:
                    f.write(f"{g}: {e[g]}\n")
                f.write("\n")
        return