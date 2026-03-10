# spectrumdb_response.py
# -*- coding: utf-8 -*-

from .models import *

class SpectrumDBResponseParser:
    @staticmethod
    def parse_init(resp_json):
        return InitResponse(resp_json)
    @staticmethod
    def parse_register(resp_json):
        return RegisterResponse(resp_json)
    @staticmethod
    def parse_available(resp_json):
        return AvailableSpectrumResponse(resp_json)
    @staticmethod
    def parse_notify(resp_json, channel):
        return NotifyResponse(resp_json, channel)

