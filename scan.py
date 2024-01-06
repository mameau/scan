#!/usr/bin/env python3

import os
import argparse
from lib.config import Config

systems = ['mame', 'mamesl','generic','pico8']
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
            from lib.output.mister import Mister
            output = Mister(sdroot="", system=cfg)
        elif output_mode == "pegasus":
            from lib.output.pegasus import Pegasus
            output = Pegasus()
        elif output_mode == "screen":
            from lib.output.screen import Screen
            output = Screen()
        elif output_mode == "yaml":
            from lib.output.yaml import YAML
            output = YAML()
        else:
            from lib.output.json import JSON
            output = JSON()
    else:
        print(f"Unsupported output mode: {output_mode}")
        exit()

    ### MAME
    if system == "mame":
        from lib.input.mame import MAME
        mame = MAME(output=output)
        dataset = mame.scan()
        sysconfig = mame.sysconfig

    elif system == "pico8":
        from lib.input.pico8 import PICO8
        pico8 = PICO8()
        dataset = pico8.scan()
        sysconfig = pico8.sysconfig

    else:
        if not cfg:
            print("--cfg is required")
            return

        ### File
        if system == "generic": 
            from lib.input.generic import Generic
            generic = Generic(mode=mode, system=cfg, output=output)
            dataset = generic.scan()
            sysconfig = generic.sysconfig
            system = cfg

        ### MAME Software Lists
        elif system == "mamesl":
            from lib.input.mamesl import MAMESL
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
    parser_input = parser.add_argument_group(title='input')
    parser_output = parser.add_argument_group(title='output')
    # input
    parser_input.add_argument('--system', required=True, type=str, default=None, help='scan a system', choices=systems)
    parser_input.add_argument('--cfg', type=str, help='system cfg')
    parser_input.add_argument('--mode', type=str, default="file" , help='software list match mode', choices=modes)
    # output
    parser_output.add_argument('--output-mode', type=str, default="json" , help='output mode', choices=output_modes)
    args = parser.parse_args()

    main(args)
