# bs.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice
from spectrumdb.req_models import *
from spectrumdb.models import *
from uciapp_manager import UCIReader
from log import write_log

class BS(BaseDevice):
    def __init__(self, config, db):
        BaseDevice.__init__(self, config)
        self.db = db
        self.version = '1.0'
        self._deviceDesc = deviceDesc()
        self._location = location()
        self._masterDeviceDesc = masterDeviceDesc()
        self._masterDeviceLocation = masterDeviceLocation()
        self._deviceOwner = deviceOwner()
        self._antennaCharacteristics = antennaCharacteristics()
        self._spectra = spectra()
        self.init_resp = None
        self.register_resp = None
        self.available_resp = None
        self.notify_resp = None

    def apply_channel(self):
        pass
    def uci_load(self, uci):
        _reqfile = 'paws'
        self._deviceDesc.uci_load(uci, _reqfile)
        write_log(self._deviceDesc)
        self._location.uci_load(uci, _reqfile)
        write_log(self._location)
        self._masterDeviceDesc.uci_load(uci, _reqfile)
        write_log(self._masterDeviceDesc)
        self._masterDeviceLocation.uci_load(uci, _reqfile)
        write_log(self._masterDeviceLocation)
        self._deviceOwner.uci_load(uci, _reqfile)
        write_log(self._deviceOwner)
        self._antennaCharacteristics.uci_load(uci, _reqfile)
        write_log(self._antennaCharacteristics)

    def uci_update(self, uci):
        _respfile = 'paws'
        if not self.available_resp == None:
            self.available_resp.uci_update(uci, _respfile)
        self._spectra.uci_update(uci, _respfile)

 

