# base_device.py
# -*- coding: utf-8 -*-

class BaseDevice(object):
    def __init__(self, _devicetype):
        self.devicetype = _devicetype
        self.channel = None

    def apply_channel(self, _channel):
        self.channel = _channel
