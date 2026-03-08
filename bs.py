# bs.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice

class BS(BaseDevice):
    def __init__(self, config, db):
        BaseDevice.__init__(self, config)
        self.db = db

    def connect_db(self):
        init = self.db.init_req(self.config)
        reg  = self.db.register_req(self.config)
        avail = self.db.avail_req(self.config)
        return avail

    def run(self):
        resp = self.connect_db()
        channel = resp["channel"]
        self.apply_channel(channel)
        return channel
