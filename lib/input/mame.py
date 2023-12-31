#!/usr/bin/env python3

import os
import re
import subprocess
from lxml import etree

import lib.logger as logger
from lib.config import Config

class MAME():
    def __init__(self, output=None):
        self.config = Config()
        self.system = 'mame'
        self.sysfile = os.path.join(self.config.config_dir_systems,'%s.yaml' % self.system)
        self.sysconfig = self.config.read_config_system(self.sysfile, output.vars())
        return

    def getxml(self):
        """ read the mameinfo.xml into memory """

        # read in data directly from the mame executable
        p = subprocess.Popen(["mame", "-listxml"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        xmlfile, xmlerr = p.communicate()

        if xmlfile is not None:
            logger.Logger()._log("Received data from mame")
            x = etree.fromstring(xmlfile)
            return x
        else:
            logger.Logger()._log("No data received from mame")
            exit()
        return None

    def searchxml(self, terms):
        """ use xpaths to find the game metadata """

        logger.Logger()._log("Total titles found: %d" % len(terms))

        # read the mame xml
        data = self.getxml()

        # out data dict
        mindata = {}

        # find all the machines and check if we have them in our filelist
        machine_data = data.findall('machine')
        for element in machine_data:
            if element.attrib['name'] in terms.keys():
                game_name = element.attrib['name']
                filename = terms[element.attrib['name']]
                try:
                    description = element.xpath('description')[0].text
                except IndexError:
                    description = ""
                try:
                    year = element.xpath('year')[0].text
                except IndexError:
                    year = ""
                try:
                    manufacturer = element.xpath('manufacturer')[0].text
                except IndexError:
                    manufacturer = ""
                try:
                    driver_status = element.xpath('driver/@status')[0]
                except IndexError:
                    driver_status = ""
                try:
                    display_orientation = element.xpath('display[@tag="screen"]/@rotate')[0]
                except IndexError:
                    display_orientation = 0
                try:
                    players = element.xpath('input/@players')[0]
                except IndexError:
                    players = 0

            mindata[game_name] = {
                'description' : description,
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
        logger.Logger()._log("Reading items from %s" % path)
        for root, dirs, files in os.walk(path):
            for filename in files:
                abspath = os.path.join(root,filename)
                name = os.path.splitext(filename)[0]
                if os.path.exists(abspath):
                    filelist[name]=(abspath)
                    #_log("adding %s" % abspath)
        logger.Logger()._log(" Found %d items" % len(filelist))
        return filelist

    def mamepaths(self, s, d=";"):
        """ split a string on delim """
        return s.split(d)

    def scan(self):
        runstart = logger.Logger().getnow()
        mameinifile = os.path.expanduser(self.sysconfig['ini'])

        start = logger.Logger().getnow()
    
        mameconfig = self.config.read_config_generic(mameinifile)

        logger.Logger().timestr(logger.Logger().getnow() - start)

        itempaths = self.mamepaths(mameconfig['rompath'])
        itemlist = {}
        for itempath in itempaths:
            start = logger.Logger().getnow()
            itemlist.update(self.scanpath(itempath))
            logger.Logger().timestr(logger.Logger().getnow() - start)

        start = logger.Logger().getnow()
        dataset = self.searchxml(itemlist)
        logger.Logger()._log("Summary")
        logger.Logger().timestr(logger.Logger().getnow() - runstart)
        return dataset
