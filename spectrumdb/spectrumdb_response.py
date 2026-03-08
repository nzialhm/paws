# spectrumdb_response.py
# -*- coding: utf-8 -*-

from .models import *

class SpectrumDBResponseParser:
    @staticmethod
    def parse_init(resp_json):
        rulesets = resp_json.get("rulesetIds", [])
        return InitResponse(rulesets)
    @staticmethod
    def parse_register(resp_json):
        device_id = resp_json.get("deviceId")
        return RegisterResponse(device_id)
    @staticmethod
    def parse_available(resp_json):
        spectrum_list = []
        for spec in resp_json.get("spectrumSchedules", []):
            for profile in spec.get("spectra", []):
                spectrum_list.append(
                    SpectrumProfile(
                        frequency=profile.get("frequency"),
                        bandwidth=profile.get("bandwidth"),
                        max_eirp=profile.get("maxEirp")
                    )
                )
        expire_time = resp_json.get("expireTime")
        return AvailableSpectrumResponse(
            profiles=spectrum_list,
            expire_time=expire_time
        )
