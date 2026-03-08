# models.py
# -*- coding: utf-8 -*-

class InitResponse:
    def __init__(self, ruleset_ids):
        self.ruleset_ids = ruleset_ids
class RegisterResponse:
    def __init__(self, device_id):
        self.device_id = device_id
class SpectrumProfile:
    def __init__(self, frequency, bandwidth, max_eirp):
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.max_eirp = max_eirp
class AvailableSpectrumResponse:
    def __init__(self, profiles, expire_time):
        self.profiles = profiles
        self.expire_time = expire_time
