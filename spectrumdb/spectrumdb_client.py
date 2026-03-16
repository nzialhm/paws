# spectrumdb_client.py
# -*- coding: utf-8 -*-

import json
import re
import urllib2
from spectrumdb_response import SpectrumDBResponseParser
from models import Channel
from .req_models import *
from uciapp_manager import UCIReader

# 유니코드 딕셔너리를 utf-8 딕셔너리로 변환하는 함수
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def fix_invalid_json(resp_data):
    
    if not resp_data:
        return resp_data
    # [ ,  → [
    resp_data = re.sub(r'\[\s*,', '[', resp_data)
    # , ] → ]
    resp_data = re.sub(r',\s*\]', ']', resp_data)
    # , } → }
    resp_data = re.sub(r',\s*\}', '}', resp_data)
    return resp_data

class SpectrumDB(object):
    def __init__(self, server_url):
        self.server_url = server_url
        self.id = 1
        # windows
        uci = UCIReader(uci_dir='.\\config')
        # linux openwrt
        # uci = UCIReader(uci_dir='/etc/config')
        self.jsonrpc = uci.get('paws', 'global', 'jsonrpc')
        self.headers = {
            "Content-Type": "application/json"
        }

    def _post(self, method, payload):
        body = {
            "jsonrpc": str(self.jsonrpc),
            "method": method,
            "params": payload,
            "id": '{:0>6}'.format(self.id)
        }
        self.id = self.id+1
        data = json.dumps(body)
        req = urllib2.Request(
            self.server_url,
            data,
            self.headers
        )
        response = urllib2.urlopen(req)
        resp_data = fix_invalid_json(response.read())
        print(resp_data)
        if not resp_data:
            raise Exception("Empty response from Spectrum DB")
        resp_json = byteify(json.loads(resp_data))
        if "result" in resp_json:
            return resp_json["result"]
        raise Exception("PAWS DB Error: %s" % resp_json)

    # -------------------------
    # INIT
    # -------------------------

    def init_req(self, device):
        payload = {
                "version": str(device.version),
                "type": "INIT_REQ",
                "deviceDesc": device._deviceDesc.to_dict(),
                "location": device._location.to_dict()
            }
        resp = self._post(
            "spectrum.paws.init",
            payload
        )
        return SpectrumDBResponseParser.parse_init(resp)

    # -------------------------
    # REGISTER
    # -------------------------
    def register_req(self, device):
        payload = {
            "version": str(device.version),
            "type": "REGISTRATION_REQ",
            "deviceDesc": device._deviceDesc.to_dict(),
            "location": device._location.to_dict(),
            "deviceOwner": device._deviceOwner.to_dict(),
            "antennaCharacteristics": device._antennaCharacteristics.to_dict()
        }
        resp = self._post(
            "spectrum.paws.register",
            payload
        )
        return SpectrumDBResponseParser.parse_register(resp)

    # -------------------------
    # AVAILABLE
    # -------------------------

    def avail_req(self, device):
        payload = {
            "version": str(device.version),
            "type": "AVAIL_SPECTRUM_REQ",
            "deviceDesc": device._deviceDesc.to_dict(),
            "location": device._location.to_dict(),
            "masterDeviceDesc": device._masterDeviceDesc.to_dict(),
            "masterDeviceLocation": device._masterDeviceLocation.to_dict(),
            "deviceOwner": device._deviceOwner.to_dict(),
            "antennaCharacteristics": device._antennaCharacteristics.to_dict()
        }
        resp = self._post(
            "spectrum.paws.getSpectrum",
            payload
        )
        return SpectrumDBResponseParser.parse_available(resp)

    # -------------------------
    # USE NOTIFY
    # -------------------------

    def notify_req(self, device):
        payload = {
                "version": str(device.version),
                "type": "SPECTRUM_USE_NOTIFY",
                "deviceDesc": device._deviceDesc.to_dict(),
                "location": device._location.to_dict(),
                "antennaCharacteristics": device._antennaCharacteristics.to_dict(),
                "masterDeviceDesc": device._masterDeviceDesc.to_dict(),
                "masterDeviceLocation": device._masterDeviceLocation.to_dict(),
                "spectra": device._spectra.to_dict()
            }
        resp = self._post(
            "spectrum.paws.notifySpectrumUse",
            payload
        )
        return SpectrumDBResponseParser.parse_notify(resp, device.channel)
