# bs.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice

class BS(BaseDevice):
    def __init__(self, config, db):
        BaseDevice.__init__(self, config)
        self.db = db

    def apply_channel(self):
        pass
