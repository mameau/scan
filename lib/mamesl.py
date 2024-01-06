#!/usr/bin/env python3

import os
import re
import subprocess
import glob
from lxml import etree

from lib.logger import Logger
from lib.config import Config

logger = Logger()

class MAMESL():
    def __init__(self, mode='file', system=None, output=None):
        self.config = Config()

        self.system = system
        self.mode = mode
        self.sysfile = os.path.join(self.config.config_dir_systems,'%s.yaml' % system)
        self.sysconfig = self.config.read_config_system(self.sysfile, output.vars())
        return

    def getxml(self):
        """ read the mameinfo.xml into memory """
        software_lists = []
        for hashpath in self.hashpaths:
            thashpath = os.path.expanduser(os.path.join(hashpath,"%s.xml" % self.system))
            if os.path.exists(thashpath):
                software_lists.append(thashpath)

        for software_list in software_lists:
            xmlfile = open(software_list,'r')
            if xmlfile is not None:
                logger._log("Received data from mame")
                x = etree.parse(xmlfile)
                return x.getroot()
            else:
                logger._log("No data received from mame")
            return None

    def searchxml(self):
        """ use xpaths to find the game metadata """

        terms = self.itemlist

        logger._log("Total titles found: %d" % len(terms))

        # read the mame xml
        data = self.getxml()

        # out data dict
        mindata = {}

        # find all the machines and check if we have them in our filelist)
        if data is None:
            return mindata
        machine_data = data.findall('software')

        for element in machine_data:
            if element.attrib['name'] in terms.keys():
                game_name = element.attrib['name']
                filename = terms[element.attrib['name']]
                try:
                    description = element.xpath('description')[0].text
                except:
                    description = ""

                try:
                    year = element.xpath('year')[0].text
                except:
                    year = "????"
                try:
                    manufacturer = element.xpath('publisher')[0].text
                except:
                    manufacturer = "unknown"
                try:
                    driver_status = element.xpath('driver/@status')[0]
                except:
                    driver_status = "good"
                try:
                    display_orientation = element.xpath('display[@tag="screen"]/@rotate')[0]
                except:
                    display_orientation = 0 
                try:
                    players = element.xpath('input/@players')[0]
                except:
                    players = 0 


                game_data = {'name':'','ext':''}
                dataareas = element.xpath('part/dataarea')
                for dataarea in dataareas:
                    roms = dataarea.findall('rom')

                    if len(roms) == 1:
                        for rom in roms:

                            if "name" in rom.attrib:
                                rom_ext = os.path.splitext(rom.attrib['name'])[1][1:] or None

                                # check if we have a compatible rom extension
                                # eventually have byte handlers here
                                if not rom_ext in self.extensions:
                                    rom_ext = self.extensions[0]

                                game_data['name'] = rom.attrib['name']
                                game_data['ext'] = rom_ext

                                #logger._log("%s | %s | %s.%s" % (rom.attrib["name"], game_name, description, self.sysconfig['extension']))

                    else:
                        #logger._log("We do not support multi-chip roms at the moment")
                        pass


                mindata[game_name] = {
                    'name' : description,
                    'description' : description,
                    'name_rom' : "%s" % game_name,
                    'name_pretty' : "%s (%s).%s" % (description, game_name, game_data['ext']),
                    'name_sl'     : game_data["name"],
                    'rom_abspath' : terms[game_name],
                    'year' : year,
                    'manufacturer' : manufacturer,
                    'driver_status' : driver_status,
                    'display_orientation' : display_orientation,
                    'players' : players,
                }

        return mindata

    def scanpath(self, path):
        """ walk mame rompaths and return a list of files """
        filelist = {}
        logger._log("Reading items from %s" % path)
        abspath = ""
        name = ""
        for root, dirs, files in os.walk(path):
            if self.mode == 'dir':
                for dirname in dirs:
                    abspath = os.path.join(root,dirname)
                    name = dirname
                    if os.path.exists(abspath):
                        filelist[name] = abspath
            elif self.mode == 'file':
                for filename in files:
                    abspath = os.path.join(root,filename)
                    name = os.path.splitext(filename)[0]
                    if os.path.exists(abspath):
                        filelist[name] = abspath
            elif self.mode == 'file-parent':
                for filename in files:
                    abspath = os.path.join(root,filename)
                    name = os.path.basename(root)
                    if os.path.exists(abspath):
                        filelist[name] = abspath

        logger._log(" Found %d items" % len(filelist))
        return filelist

    def mamepaths(self, s, d=";"):
        """ split a string on delim """
        return s.split(d)

    def scan(self):
        logger.runstart()

        if self.sysconfig is None:
            logger._log("Software list config not found")
            return None
        self.system = self.sysconfig['name']

        self.extensions = self.sysconfig['extensions'].split()

        self.mameinifile = self.sysconfig['ini']
        self.mameinifile = self.config.expand_user(self.mameinifile)

        logger.start()
        mameconfig = self.config.read_config_generic(self.mameinifile)
        logger.end()

        itempaths = self.mamepaths(self.sysconfig['rom_dir'])
        self.hashpaths = [os.path.join(os.path.expanduser(self.sysconfig['data_dir']))] + mameconfig['hashpath'].split(";")

        self.itemlist = {}
        for itempath in itempaths:
            logger.start()
            self.itemlist.update(self.scanpath(itempath))

        logger.start()
        dataset = self.searchxml()
        logger.end()


        logger.summary()
        logger.runend()
        return dataset
