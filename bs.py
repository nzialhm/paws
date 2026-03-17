# bs.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice
from spectrumdb.req_models import *
from spectrumdb.models import *
from uciapp_manager import UCIReader

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
        self.version = uci.get(_reqfile, 'global', 'version')
        self._deviceDesc.uci_load(uci, _reqfile)
        self._location.uci_load(uci, _reqfile)
        self._masterDeviceDesc.uci_load(uci, _reqfile)
        self._masterDeviceLocation.uci_load(uci, _reqfile)
        self._deviceOwner.uci_load(uci, _reqfile)
        self._antennaCharacteristics.uci_load(uci, _reqfile)
        self._spectra.uci_load(uci, _reqfile)

    def uci_update(self, uci):
        _respfile = 'paws'
        if not self.init_resp == None:
            self.init_resp.uci_update(uci, _respfile)
        if not self.register_resp == None:
            self.register_resp.uci_update(uci, _respfile)
        if not self.available_resp == None:
            self.available_resp.uci_update(uci, _respfile)
        if not self.notify_resp == None:
            self.notify_resp.uci_update(uci, _respfile)
        self._spectra.uci_update(uci, _respfile)

 

