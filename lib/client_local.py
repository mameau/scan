#!/usr/bin/env python3
import shutil

""" local directory client """

#can mount local with sshfs

class ClientDIR():
    def __init__(self, mountpoint):
        self.mountpoint = mountpoint or None
        return

    def mkendpoint(self):
        return

    def put(self, source, dest):
        """ put files for client """
        shutil.copy2(source, dest)
        return

    def get(self):
        """ get files from client """
        return

    def delete(self):
        """ delete files from client """
        return