#!/usr/bin/env python3

import os
import argparse

# libs
import lib.mame as mame
import lib.mamesl as mamesl
#import lib.pico8 as pico8
#import lib.pegasus as pegasus
import lib.config as config

def init():
    config_paths = ['cfg','_cache']
    for path in config_paths:
        abs = os.path.join(config.Config().config_dir, path)
        if not os.path.exists(abs):
            os.mkdir(abs)

def main(args):
    system = args.system
    sl = args.sl
    mode = args.mode

    init()
    if system is None:
        print("need a system")

    ### MAME
    if system == "mame":
        mame.MAME().scan()

    ### PICO8
    if system == "pico8":
        pico8.PICO8().scan()

    ### MAME Software Lists
    if system == "mamesl":
        if not sl:
            print("--sl not passed")
            return

        sysfile = os.path.join(config.Config().config_dir,'cfg','%s.yaml' % sl)
        sysconfig = config.Config().read_config_system(sysfile)

        msl  = mamesl.MAMESL()
        dataset = msl.scan(sysconfig, mode)

        if  args.mister:
            mstr = mister.Mister()

            # local dir mode
            mountpoint = os.path.join('/mnt/sshfs/mister', mstr.sdroot, sysconfig['mister_core'])
            mstr.mkdir(mountpoint)
            client = client_local.ClientDIR(mountpoint)

            a = archive.Archive()
            a.extract(dataset, client)
        if args.pegasus_fe:
            print("blah")

    else:
        print("Unsupported system")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan a system')
    parser.add_argument('--system', required=True, type=str, default=None, help='scan in a system')
    parser.add_argument('--sl', type=str, help='software list shortname')
    parser.add_argument('--mode', type=str, default="file" , help='software list match mode (file|dir)')
    parser.add_argument('--mister', type=bool, default=False, help='unpack to MiSTer')
    parser.add_argument('--pegasus-fe', type=bool, default=False, help='pegasus frontend')
    args = parser.parse_args()


    main(args)
