# paws_fsm.py
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from spectrumdb.models import *
from spectrumdb.req_models import *
from uciapp_manager import UCIReader
from log import write_log

class PawsFSM(object):
    def __init__(self, device, uci):
        self.channel_id=0
        self.device = device
        self.state = "UCIINIT"
        self.uci = uci
        self.test_len1 = 0
        self.test_geo_lati =[]
        self.test_geo_lati.append('37.48055')
        self.test_geo_lati.append('35.87490')
        self.test_geo_lati.append('36.37376')
        self.test_geo_long =[]
        self.test_geo_long.append('126.88384')
        self.test_geo_long.append('128.61777')
        self.test_geo_long.append('127.31844')

        self.test_len2 = 0
        self.test_ksDeviceType =[]
        self.test_ksDeviceType.append('Portable Master')
        self.test_ksDeviceType.append('Fixed Master')
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
                self.device.uci_load(self.uci)
                self.state = "INIT"
            # -----------------
            # WAITRETRY
            # -----------------
            elif self.state == "WAITRETRY":
                write_log("STATE: WAITRETRY")
                time.sleep(5)
                self.uci.set('paws', 'dev', 'ksDeviceType', self.test_ksDeviceType[self.test_len1])
                self.uci.set('paws', 'dev', 'geo_lati', self.test_geo_lati[self.test_len2])
                self.uci.set('paws', 'dev', 'geo_long', self.test_geo_long[self.test_len2])

                self.test_len1 = self.test_len1 + 1
                if self.test_len1 > 1:
                    self.test_len1 = 0
                    
                self.test_len2 = self.test_len2 + 1
                if self.test_len2 > 2:
                    self.test_len2 = 0

                self.state = "UCILOAD"
                
            # -----------------
            # INIT
            # -----------------
            elif self.state == "INIT":
                write_log("STATE: INIT")
                self.device.init_resp = None
                self.device.register_resp = None
                self.device.available_resp = None
                self.device.availablebatch_resp = None
                self.device.notify_resp = None
                self.device.channel = None
                self.device.expire_time="2026-00-01 01:00:00"
                try:
                    self.device.init_resp = self.device.db.init_req(self.device)
                    if isinstance(self.device.init_resp, InitResponse):
                        write_log(self.device.init_resp)
                        self.state = "REGISTER"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("INIT ERROR: %s" % e)
                    self.state = "WAITRETRY"
            # -----------------
            # REGISTER
            # -----------------
            elif self.state == "REGISTER":
                write_log("STATE: REGISTER")
                self.device.register_resp = None
                try:
                    self.device.register_resp = self.device.db.register_req(self.device)
                    if isinstance(self.device.register_resp, RegisterResponse):
                        write_log(self.device.register_resp)
                        self.state = "AVAILABLE"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("REGISTER ERROR: %s" % e)
                    self.state = "WAITRETRY"
            # -----------------
            # AVAILABLE
            # -----------------
            elif self.state == "AVAILABLE":
                write_log("STATE: AVAILABLE")
                self.device.available_resp = None
                try:
                    self.device.available_resp = self.device.db.avail_req(self.device)
                    if isinstance(self.device.available_resp, AvailableSpectrumResponse):
                        write_log(self.device.available_resp)
                        size = len(self.device.available_resp.profiles)
                        if size > 0:
                            self.state = "USENOTIFY"
                        else:
                            self.state = "WAITRETRY"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("AVAILABLE ERROR: %s" % e)
                    self.state = "WAITRETRY"
            # -----------------
            # AVAILABLE BATCH
            # -----------------
            elif self.state == "AVAILABLEBATCH":
                write_log("STATE: AVAILABLEBATCH")
                self.device.availablebatch_resp = None
                try:
                    self.device.availablebatch_resp = self.device.db.availbatch_req(self.device)
                    if isinstance(self.device.availablebatch_resp, AvailableBatchSpectrumResponse):
                        write_log(self.device.availablebatch_resp)
                        size = len(self.device.availablebatch_resp.profiles)
                        if size > 0:
                            self.state = "USENOTIFY"
                        else:
                            self.state = "WAITRETRY"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("AVAILABLEBATCH ERROR: %s" % e)
                    self.state = "WAITRETRY"
                
            # -----------------
            # USENOTIFY
            # -----------------
            elif self.state == "USENOTIFY":
                write_log("STATE: USENOTIFY")
                self.device.notify_resp = None
                self.device.expire_time="2026-00-01 01:00:00"
                if self.device.available_resp.profiles:
                    self.device.channel = self.device.available_resp.profiles[0]
                    self.device._spectra.set_channelinfo(self.device.channel)
                    try:
                        self.device.notify_resp = self.device.db.notify_req(self.device)
                        if isinstance(self.device.notify_resp, NotifyResponse):
                            write_log(self.device.notify_resp)
                            self.device.expire_time=self.device.notify_resp.select_channel.stopTime
                            self.channel_id=self.device.notify_resp.select_channel.channel_id
                            self.state = "UCIUPDATE"
                        else:
                            self.state = "WAITRETRY"
                    except Exception as e:
                        write_log("USENOTIFY ERROR: %s " % e)
                        self.state = "WAITRETRY"
                else:
                    write_log("USENOTIFY ERROR: USE NOT CHANNEL !!")
                    self.state = "WAITRETRY"

            # -----------------
            # UCIUPDATE
            # -----------------
            elif self.state == "UCIUPDATE":
                write_log("STATE: UCIUPDATE")
                self.device.uci_update(self.uci)
                self.state = "OPERATE"
            # -----------------
            # OPERATE
            # -----------------
            elif self.state == "OPERATE":
                write_log("STATE: OPERATE")
                _continuecount = self.uci.get('paws', 'global', 'continuecount')
                if type(_continuecount) == int:
                    if _continuecount > 0 :
                        _continuecount = _continuecount - 1
                        self.uci.set('paws', 'global', 'continuecount', _continuecount)
                        write_log("Spectrum request again")
                        self.state = "WAITRETRY"

                if self._is_expired():
                    write_log("Spectrum expired request again")
                    self.state = "AVAILABLE"
                    time.sleep(10)

    # -----------------
    # expire check
    # -----------------
    def _is_expired(self):
        if not self.device.expire_time:
            return True
        expire = datetime.strptime(
            self.device.expire_time,
            "%Y-%m-%d %H:%M:%S"
        )
        return datetime.utcnow() >= expire
