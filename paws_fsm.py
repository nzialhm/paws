# paws_fsm.py
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from spectrumdb.models import *

class PawsFSM(object):
    def __init__(self, device):
        self.channel_id=0
        self.device = device
        self.state = "UCILOAD"
    def run(self):
        while True:
            # -----------------
            # UCILOAD
            # -----------------
            if self.state == "UCILOAD":
                print("STATE: UCILOAD")
                self.device.uci_load()
                self.state = "INIT"
            # -----------------
            # WAITRETRY
            # -----------------
            elif self.state == "WAITRETRY":
                print("STATE: WAITRETRY")
                time.sleep(5)
                self.state = "INIT"
                
            # -----------------
            # INIT
            # -----------------
            elif self.state == "INIT":
                print("STATE: INIT")
                self.device.init_resp = None
                self.device.register_resp = None
                self.device.available_resp = None
                self.device.notify_resp = None
                self.device.channel = None
                self.device.expire_time="2026-00-01 01:00:00"
                try:
                    self.device.init_resp = self.device.db.init_req(self.device)
                    if isinstance(self.device.init_resp, InitResponse):
                        print(self.device.init_resp)
                        self.state = "REGISTER"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    print("INIT ERROR:", e)
                    self.state = "WAITRETRY"
            # -----------------
            # REGISTER
            # -----------------
            elif self.state == "REGISTER":
                print("STATE: REGISTER")
                self.device.register_resp = None
                try:
                    self.device.register_resp = self.device.db.register_req(self.device)
                    if isinstance(self.device.register_resp, RegisterResponse):
                        print(self.device.register_resp)
                        self.state = "AVAILABLE"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    print("REGISTER ERROR:", e)
                    self.state = "WAITRETRY"
            # -----------------
            # AVAILABLE
            # -----------------
            elif self.state == "AVAILABLE":
                print("STATE: AVAILABLE")
                self.device.available_resp = None
                try:
                    self.device.available_resp = self.device.db.avail_req(self.device)
                    if isinstance(self.device.available_resp, AvailableSpectrumResponse):
                        print(self.device.available_resp)
                        size = len(self.device.available_resp.profiles)
                        if size > 0:
                            print(size)
                            self.state = "USENOTIFY"
                        else:
                            self.state = "WAITRETRY"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    print("AVAILABLE ERROR:", e)
                    self.state = "WAITRETRY"
                
            # -----------------
            # USENOTIFY
            # -----------------
            elif self.state == "USENOTIFY":
                print("STATE: USENOTIFY")
                self.device.notify_resp = None
                self.device.expire_time="2026-00-01 01:00:00"
                if self.device.available_resp.profiles:
                    self.device.channel = self.device.available_resp.profiles[0]
                print(self.device.channel)
                self.device._spectra.set_channelinfo(self.device.channel)
                try:
                    self.device.notify_resp = self.device.db.notify_req(self.device)
                    if isinstance(self.device.notify_resp, NotifyResponse):
                        print(self.device.notify_resp)
                        self.device.expire_time=self.device.notify_resp.select_channel.stopTime
                        self.channel_id=self.device.notify_resp.select_channel.channel_id
                        self.state = "UCIUPDATE"
                    else:
                        self.state = "WAITRETRY"
                except Exception as e:
                    print("USENOTIFY ERROR:", e)
                    self.state = "WAITRETRY"
            # -----------------
            # UCIUPDATE
            # -----------------
            elif self.state == "UCIUPDATE":
                print("STATE: UCIUPDATE")
                self.device.uci_update()
                self.state = "OPERATE"
            # -----------------
            # OPERATE
            # -----------------
            elif self.state == "OPERATE":
                print("STATE: OPERATE")
                if self._is_expired():
                    print("Spectrum expired → request again")
                    self.state = "AVAILABLE"
                time.sleep(5)

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
