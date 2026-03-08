# cpe.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice

class CPE(BaseDevice):
    def __init__(self, config):
        BaseDevice.__init__(self, config)

    def wait_bs_channel(self):
        print("Waiting BS channel...")
        # 실제 구현
        # beacon scan
        # local socket
        # rpc
        channel = "BS_CHANNEL"
        return channel


    def run(self):
        channel = self.wait_bs_channel()
        self.apply_channel(channel)
