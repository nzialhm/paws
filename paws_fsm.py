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
                init_resp = self.device.db.init_req(self.device.config)
                print(init_resp)
                self.state = "REGISTER"
            # -----------------
            # REGISTER
            # -----------------
            elif self.state == "REGISTER":
                print("STATE: REGISTER")
                register_resp = self.device.db.register_req(self.device.config)
                print(register_resp)
                self.state = "AVAILABLE"
            # -----------------
            # AVAILABLE
            # -----------------
            elif self.state == "AVAILABLE":
                print("STATE: AVAILABLE")
                available_resp = self.device.db.avail_req(self.device.config)
                print(available_resp)
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
