#!/usr/bin/env python3

import os
import argparse
from lib.config import Config

formats = ['mame', 'mamesl','generic','pico8']
output_modes = ['mister', 'pegasus','json','yaml','screen']
config_paths = ['system','_cache']

def main(args):
    output_mode = args.output_mode
    system = args.system

    config = Config()
    config.read_config_main()
    mainconfig = config.config_main

    output = ""

    ### OUTPUT modes

    if output_mode in output_modes:
        if  output_mode == "mister":
            from lib.output.mister import Mister
            output = Mister(sdroot="", system=system)
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

    sysfile = os.path.join(config.config_dir_systems,f"{system}.yaml")
    if os.path.exists(sysfile):
        sysconfig = config.read_config_system(sysfile, output.vars())
        if "format" in sysconfig.keys():
            format = sysconfig["format"]
        else:
            print(f"missing format key for {system}")

        ### MAME
        if format in formats:
            if format == "mame":
                from lib.input.mame import MAME
                mame = MAME(output=output)
                dataset = mame.scan()
                sysconfig = mame.sysconfig

            elif format == "pico8":
                from lib.input.pico8 import PICO8
                pico8 = PICO8()
                dataset = pico8.scan()
                sysconfig = pico8.sysconfig

            ### File
            elif format == "generic": 
                from lib.input.generic import Generic
                generic = Generic(system=system, output=output)
                dataset = generic.scan()
                sysconfig = generic.sysconfig

            ### MAME Software Lists
            elif format == "mamesl":
                from lib.input.mamesl import MAMESL
                mamesl = MAMESL(system=system, output=output)
                dataset = mamesl.scan()
                sysconfig = mamesl.sysconfig
        else:
            print("Unsupported system")
            exit()

    else:
        print(f"system config not doing {system}")

    #push dataset to output module
    output.collection(sysconfig)
    output.entry(dataset)
    output.dump(system)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan a system')
    parser_input = parser.add_argument_group(title='input')
    parser_output = parser.add_argument_group(title='output')
    # input
    parser_input.add_argument('--system', type=str, help='system system')
    # output
    parser_output.add_argument('--output-mode', type=str, default="json" , help='output mode', choices=output_modes)
    args = parser.parse_args()

    main(args)
