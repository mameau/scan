#!/usr/bin/env python3

# dependant on py7zr because i'm lazy
# doesn't handle standard zip files??
#import py7zr

import zipfile
import tempfile
import os
import shutil

import lib.logger as logger

class Archive():
    def __init__(self):
        self.archive_tmp = tempfile.TemporaryDirectory(dir=tempfile.gettempdir())
        return

    def open_ro(self, filename):
        #self.archive = py7zr.SevenZipFile(filename, mode='r')
        self.archive = zipfile.ZipFile(filename, mode='r')

    def close(self):
        self.archive.close()

    def getinfo(self):
        return

    def valid_filename(self, validate):
        for string in ['?','/','\\',';','*','<','>','|',':','"']:
            validate = validate.replace(string,'_')
        return validate

    def extract(self, dataset, client):

        for item in dataset.keys():
            logger.Logger()._log("Processing %s from %s" % (dataset[item]['description'], dataset[item]['rom_abspath']))
            self.open_ro(dataset[item]['rom_abspath'])
            #allfiles = self.archive.getnames() #py7zr
            allfiles = self.archive.namelist()
            targets = []
            if dataset[item]['name_sl'] in allfiles:
                src = os.path.join(self.archive_tmp.name,dataset[item]['name_sl'])
                dest = os.path.join(client.mountpoint,self.valid_filename(dataset[item]['name_pretty']))

                if not os.path.exists(dest):
                    self.archive.extract(dataset[item]['name_sl'], path=self.archive_tmp.name)

                if os.path.exists(src):
                    client.put(src, dest)

            self.close()
        return

    def test(self):
        return

    def cleanup(self):
        self.archive_tmp.cleanup()