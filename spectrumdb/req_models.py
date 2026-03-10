# req_models.py
# -*- coding: utf-8 -*-

class deviceDesc:
    def __init__(self):
        self.serialNumber="WS20-224-0000004"
        self.ksDeviceEmissionPower=20
        self.ksCertId="R-R-nZc-NZC-WS20"
        self.ksDeviceType="Portable Master"
        self.modelId="NZC-WS20"
    def to_dict(self):
        return {
            "serialNumber": self.serialNumber,
            "ksDeviceEmissionPower": self.ksDeviceEmissionPower,
            "ksCertId": self.ksCertId,
            "ksDeviceType": self.ksDeviceType,
            "modelId": self.modelId
        }

class location:
    def __init__(self):
        self.latitude = 37.586
        self.longitude = 126.8172
    def to_dict(self):
        return {
                "point": {
                    "center": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    }
                }
            }

class deviceOwner:
    def __init__(self):
        self.operator_tel = "+82 32 650 5766"

        self.adr_country = "KR"
        self.adr_region = "South Korea"
        self.adr_code = "21315"
        self.adr_street = "bupyungdearo 293"
        self.adr_locality = "bupyunggu"

        self.operator_email = "welcome@nzia.kr"
        self.operator_fn = "NZIA"

        self.owner_kind = "co"
        self.owner_fn = "NZIA"
    def to_dict(self):
        return {
                "operator": {
                    "tel": self.operator_tel,
                    "adr": {
                        "country": self.adr_country,
                        "region": self.adr_region,
                        "code": self.adr_code,
                        "street": self.adr_street,
                        "locality": self.adr_locality
                    },
                    "email": self.operator_email,
                    "fn": self.operator_fn
                },
                "owner": {
                    "kind": self.owner_kind,
                    "fn": self.owner_fn
                }
            }

class antennaCharacteristics:
    def __init__(self):
        self.heightType="AGL"
        self.height=11.0
    def to_dict(self):
        return  {
                "heightType": self.heightType,
                "height": self.height
            }

class masterDeviceDesc:
    def __init__(self):
        self.serialNumber="WS20-224-0000004"
        self.ksDeviceEmissionPower=20
        self.ksCertId="R-R-nZc-NZC-WS20"
        self.ksDeviceType="Portable Master"
        self.modelId="NZC-WS20"
    def to_dict(self):
        return  {
                "serialNumber": self.serialNumber,
                "ksDeviceEmissionPower": self.ksDeviceEmissionPower,
                "ksCertId": self.ksCertId,
                "ksDeviceType": self.ksDeviceType,
                "modelId": self.modelId
            }

class masterDeviceLocation:
    def __init__(self):
        self.latitude = 37.586
        self.longitude = 126.8172
    def to_dict(self):
        return {
                "point": {
                    "center": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    }
                }
            }

class spectra:
    def __init__(self):
        self.bandwidth=6
        self.frequencyRanges=[]
        frequencyRanges_0={}
        frequencyRanges_0["startHz"] = 536
        frequencyRanges_0["stopHz"] = 542
        frequencyRanges_0["channelId"] = 25
        self.frequencyRanges.append(frequencyRanges_0)
    def to_dict(self):
        return  {
                "bandwidth": self.bandwidth,
                "frequencyRanges": self.frequencyRanges
            }
