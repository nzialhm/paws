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
        self.select = "auto"

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
                self.select = self.uci.get('paws', 'ch', 'select')
                self.device.uci_load(self.uci)
                if self.device.blocationcheck:
                    self.state = "INIT"
                else:
                    write_log("UCILOAD location data Failed !!")
                    self.state = "WAITRETRY"
            # -----------------
            # WAITRETRY
            # -----------------
            elif self.state == "WAITRETRY":
                write_log("STATE: WAITRETRY")
                self.state = "UCIINIT"
                time.sleep(20)
                
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
                self.device.expire_time=None
                self.channel_id=0
                self.uci.set('paws', 'ch', 'current', str(self.channel_id))
                try:
                    self.device.init_resp = self.device.db.init_req(self.device)
                    if isinstance(self.device.init_resp, InitResponse):
                        write_log(self.device.init_resp)
                        self.state = "REGISTER"
                    else:
                        write_log("INIT Failed")
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
                        write_log("REGISTER Failed")
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
                            if self.select == 'auto':
                                _Channel = self.device.available_resp.profiles[0]
                                self.uci.set('paws', 'ch', 'current', str(_Channel.channel_id))
                                self.state = "USENOTIFY"
                            else:
                                self.state = "UCIUPDATE"
                        else:
                            write_log("AVAILABLE Not channel")
                            self.state = "WAITRETRY"
                    else:
                        write_log("AVAILABLE Failed")
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
                            if self.uci.get('paws', 'ch', 'select') == 'auto':
                                self.state = "USENOTIFY"
                            else:
                                self.state = "UCIUPDATE"
                        else:
                            write_log("AVAILABLEBATCH Not channel")
                            self.state = "WAITRETRY"
                    else:
                        write_log("AVAILABLEBATCH Failed")
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
                self.device.expire_time=None
                if len(self.device.available_resp.profiles)>0:
                    try:
                        _current = self.uci.get('paws', 'ch', 'current')
                        if isinstance(_current, basestring):
                            _current = int(_current)
                        if _current >= 14:
                            self.device.channel = self.device.available_resp.get_Channel(_current)
                            if self.device.channel != None:
                                self.device._spectra.set_channelinfo(self.device.channel)

                                self.device.notify_resp = self.device.db.notify_req(self.device)
                                if isinstance(self.device.notify_resp, NotifyResponse):
                                    write_log(self.device.notify_resp)
                                    self.device.expire_time=self.device.notify_resp.select_channel.stopTime
                                    self.channel_id=self.device.notify_resp.select_channel.channel_id
                                    if isinstance(self.channel_id, basestring):
                                        self.channel_id = int(self.channel_id)
                                    self.state = "UCIUPDATE"
                                else:
                                    write_log("USENOTIFY Instance Failed")
                                    self.state = "OPERATE"
                            else:
                                write_log("get Channel class - channel_id select Failed")
                                self.state = "OPERATE"
                        else:
                            write_log("Channel Arear Failed")
                            self.state = "OPERATE"
                    except Exception as e:
                        write_log("USENOTIFY ERROR: %s " % e)
                        self.state = "OPERATE"
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
                _continuetime = self.uci.get('paws', 'global', 'continuetime')
                if isinstance(_continuetime, basestring):
                    _continuetime = int(_continuetime)
                    print("_continuetime: %d" % _continuetime)

                if _continuetime == 0:
                    _reload = self.uci.get('paws', 'global', 'reload')
                    if _reload == 'y':
                        self.uci.set('paws', 'global', 'reload', 'n')
                        write_log("reload - paws again!!")
                        self.state = "UCIINIT"
                        time.sleep(10)
                    else:
                        _current = self.uci.get('paws', 'ch', 'current')
                        if isinstance(_current, basestring):
                            _current = int(_current)
                            print("current channel: %d" % _current)
                        if _current >= 14 and _current != self.channel_id:
                            self.state = "USENOTIFY"
                        else:
                            if self._is_expired():
                                write_log("Spectrum expired request again")
                                self.state = "UCIINIT"
                            time.sleep(10)
                else:
                    self.state = "UCIINIT"
                    time.sleep(_continuetime)



    # -----------------
    # expire check
    # -----------------
    def _is_expired(self):
        if not self.device.expire_time:
            return False
        expire = datetime.strptime(
            self.device.expire_time,
            "%Y-%m-%d %H:%M:%S"
        )
        return datetime.utcnow() >= expire
