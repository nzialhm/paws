# paws_netproc.py
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from spectrumdb.models import *
from spectrumdb.req_models import *
from uciapp_manager import UCIReader
from log import write_log

class PawsNetProc(object):
    def __init__(self, device, uci):
        self.device = device
        self.uci = uci

    def available_proc(self):
        # -----------------
        # AVAILABLE NET CPE
        # -----------------
        write_log("STATE: AVAILABLE NET CPE")
        available_respjson = None
        _deviceDesc = deviceDesc()
        _location = location()
        try:
            available_respjson = self.device.db.availnet_req(self.device, _deviceDesc, _location)

        except Exception as e:
            write_log("AVAILABLE NET CPE ERROR: %s" % e)
        
