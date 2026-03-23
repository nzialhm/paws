# cpe.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice

class CPE(BaseDevice):
    def __init__(self, config):
        BaseDevice.__init__(self, config)
        self.channel = ''

    def run(self):
        pass
