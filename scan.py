#!/usr/bin/env python3

import os
import argparse

# libs
from lib.mame import MAME
from lib.mamesl import MAMESL
from lib.json import JSON
#from lib.pico8 import PICO8
from lib.mister import Mister
from lib.pegasus import Pegasus
from lib.config import Config
from lib.generic import Generic
from lib.screen import Screen

systems = ['mame', 'mamesl','generic']
output_modes = ['mister', 'pegasus','json','yaml','screen']
config_paths = ['cfg','_cache']
modes = ['dir','file','file-parent']

def main(args):
    system = args.system
    mode = args.mode
    output_mode = args.output_mode
    cfg = args.cfg

    config = Config()
    config.read_config_main()
    mainconfig = config.config_main

    output = ""

    ### OUTPUT modes

    if output_mode in output_modes:
        if  output_mode == "mister":
            output = Mister(sdroot="", system=cfg)
        elif output_mode == "pegasus":
            output = Pegasus()
        elif output_mode == "screen":
            output = Screen()
        elif output_mode == "yaml":
            print("YAML is not supported yet")
            return
        else:
            output = JSON()
    else:
        print(f"Unsupported output mode: {output_mode}")
        exit()

    ### MAME
    if system == "mame":
        mame = MAME(output=output)
        dataset = mame.scan()
        sysconfig = mame.sysconfig

    else:
        if not cfg:
            print("--cfg not passed")
            return

        ### File
        if system == "generic": 
            generic = Generic(mode=mode, system=cfg, output=output)
            dataset = generic.scan()
            sysconfig = generic.sysconfig
            system = cfg

        ### MAME Software Lists
        elif system == "mamesl":
            mamesl = MAMESL(mode=mode, system=cfg, output=output)
            dataset = mamesl.scan()
            sysconfig = mamesl.sysconfig
            system = cfg

        else:
            print("Unsupported system")
            exit()

    #push dataset to output module
    output.collection(sysconfig)
    output.entry(dataset)
    output.dump(system)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan a system')
    # input
    parser.add_argument('--system', required=True, type=str, default=None, help='scan in a system')
    parser.add_argument('--cfg', type=str, help='system cfg')
    parser.add_argument('--mode', type=str, default="file" , help='software list match mode (file|dir)')
    # output
    parser.add_argument('--output-mode', type=str, default="json" , help='output to what?')
    args = parser.parse_args()


    main(args)
