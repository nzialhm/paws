# base_device.py
# -*- coding: utf-8 -*-

class BaseDevice(object):
    def __init__(self, config):
        self.config = config
        self.channel = None

    def apply_channel(self, channel):
        self.channel = channel
        print("Apply channel:", channel)
