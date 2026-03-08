# paws_fsm.py
# -*- coding: utf-8 -*-

import time
from datetime import datetime

class PawsFSM(object):
    def __init__(self, device):
        self.device = device
        self.state = "INIT"
    def run(self):
        while True:
            # -----------------
            # INIT
            # -----------------
            if self.state == "INIT":
                print("STATE: INIT")
                resp = self.device.db.init_req(self.device.config)
                self.device.rulesets = resp
                print(resp)
                self.state = "REGISTER"
            # -----------------
            # REGISTER
            # -----------------
            elif self.state == "REGISTER":
                print("STATE: REGISTER")
                resp = self.device.db.register_req(self.device.config)
                self.device.device_id = resp.device_id
                self.state = "AVAILABLE"
            # -----------------
            # AVAILABLE
            # -----------------
            elif self.state == "AVAILABLE":
                print("STATE: AVAILABLE")
                resp = self.device.db.avail_req(self.device.config)
                self.device.expire_time = resp.expire_time
                self.device.apply_channel(resp.profiles)
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
            "%Y-%m-%dT%H:%M:%S"
        )
        return datetime.utcnow() >= expire
