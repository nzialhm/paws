# req_models.py
# -*- coding: utf-8 -*-

class deviceDesc:
    def __init__(self):
        self.serialNumber="WS20-224-0000004"
        self.ksDeviceEmissionPower=20
        self.ksCertId="R-R-nZc-NZC-WS20"
        self.ksDeviceType="Portable Master"
        self.modelId="NZC-WS20"

    def uci_load(self, uci, file):
        self.serialNumber=uci.get(file, 'deviceDesc', 'serialNumber')
        self.ksDeviceEmissionPower=uci.get(file, 'deviceDesc', 'ksDeviceEmissionPower')
        self.ksCertId=uci.get(file, 'deviceDesc', 'ksCertId')
        self.ksDeviceType=uci.get(file, 'deviceDesc', 'ksDeviceType')
        self.modelId=uci.get(file, 'deviceDesc', 'modelId')

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
    
    def uci_load(self, uci, file):
        self.latitude = uci.get(file, 'location', 'latitude')
        self.longitude = uci.get(file, 'location', 'longitude')

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
    
    def uci_load(self, uci, file):
        self.operator_tel = uci.get(file, 'deviceOwner', 'operator_tel')

        self.adr_country = uci.get(file, 'deviceOwner', 'adr_country')
        self.adr_region = uci.get(file, 'deviceOwner', 'adr_region')
        self.adr_code = uci.get(file, 'deviceOwner', 'adr_code')
        self.adr_street = uci.get(file, 'deviceOwner', 'adr_street')
        self.adr_locality = uci.get(file, 'deviceOwner', 'adr_locality')

        self.operator_email = uci.get(file, 'deviceOwner', 'operator_email')
        self.operator_fn = uci.get(file, 'deviceOwner', 'operator_fn')

        self.owner_kind = uci.get(file, 'deviceOwner', 'owner_kind')
        self.owner_fn = uci.get(file, 'deviceOwner', 'owner_fn')

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
    
    def uci_load(self, uci, file):
        self.heightType=uci.get(file, 'antennaCharacteristics', 'heightType')
        self.height=uci.get(file, 'antennaCharacteristics', 'height')

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
        
    
    def uci_load(self, uci, file):
        self.serialNumber=uci.get(file, 'masterDeviceDesc', 'serialNumber')
        self.ksDeviceEmissionPower=uci.get(file, 'masterDeviceDesc', 'ksDeviceEmissionPower')
        self.ksCertId=uci.get(file, 'masterDeviceDesc', 'ksCertId')
        self.ksDeviceType=uci.get(file, 'masterDeviceDesc', 'ksDeviceType')
        self.modelId=uci.get(file, 'masterDeviceDesc', 'modelId')

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
    
    def uci_load(self, uci, file):
        self.latitude = uci.get(file, 'masterDeviceLocation', 'latitude')
        self.longitude = uci.get(file, 'masterDeviceLocation', 'longitude')

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

    def uci_load(self, uci, file):
        self.bandwidth = uci.get(file, 'spectra', 'bandwidth')
        self.frequencyRanges[0]["startHz"] = uci.get(file, 'spectra', 'startHz')
        self.frequencyRanges[0]["stopHz"] = uci.get(file, 'spectra', 'stopHz')
        self.frequencyRanges[0]["channelId"] = uci.get(file, 'spectra', 'channelId')

    def uci_update(self, uci, file):
        uci.set(file, 'spectra', 'bandwidth', self.bandwidth)
        uci.set(file, 'spectra', 'startHz', self.frequencyRanges[0]["startHz"])
        uci.set(file, 'spectra', 'stopHz', self.frequencyRanges[0]["stopHz"])
        uci.set(file, 'spectra', 'channelId', self.frequencyRanges[0]["channelId"])

    @staticmethod
    def uci_init(uci):
        _respfile = 'paws'
        uci.set(_respfile, 'spectra', 'bandwidth', '')
        uci.set(_respfile, 'spectra', 'startHz', '')
        uci.set(_respfile, 'spectra', 'stopHz', '')
        uci.set(_respfile, 'spectra', 'channelId', '')

    def set_channelinfo(self, channel):
        self.bandwidth = channel.bandwidth
        self.frequencyRanges[0]["startHz"] = channel.start_hz
        self.frequencyRanges[0]["stopHz"] = channel.stop_hz
        self.frequencyRanges[0]["channelId"] = channel.channel_id

    def to_dict(self):
        return  {
                "bandwidth": self.bandwidth,
                "frequencyRanges": self.frequencyRanges
            }
