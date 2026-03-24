# cpe.py
# -*- coding: utf-8 -*-

from base_device import BaseDevice
from spectrumdb.req_models import *
from spectrumdb.models import *
from log import write_log
import time

class CPE(BaseDevice):
    def __init__(self, _devicetype, uci):
        BaseDevice.__init__(self, _devicetype)
        self.uci = uci
        self.state = "UCIINIT"

    def run(self):
        while True:
            # -----------------
            # UCIINIT
            # -----------------
            if self.state == "UCIINIT":
                write_log("STATE: UCIINIT")
                spectra.uci_init(self.uci)
                AvailableSpectrumResponse.uci_init(self.uci)
                self.state = "UCILOAD"
            # -----------------
            # UCILOAD
            # -----------------
            if self.state == "UCILOAD":
                write_log("STATE: UCILOAD")
                self.state = "WAITRETRY"
            # -----------------
            # WAITRETRY
            # -----------------
            elif self.state == "WAITRETRY":
                write_log("STATE: WAITRETRY")
                time.sleep(20)
