# req_models.py
# -*- coding: utf-8 -*-
from log import write_log

class deviceDesc:
    def __init__(self):
        self.serialNumber="WS20-224-0000004"
        self.ksDeviceEmissionPower=20
        self.ksCertId="R-R-nZc-NZC-WS20"
        self.ksDeviceType="Portable Master"
        self.modelId="NZC-WS20"

    def uci_load(self, uci):
        self.serialNumber=uci.get('paws', 'dev', 'serialNumber') or ""
        self.ksDeviceEmissionPower = int(uci.get('paws', 'dev', 'ksDeviceEmissionPower') or 0)
        self.ksCertId=uci.get('paws', 'dev', 'ksCertId') or ""
        self.ksDeviceType=uci.get('paws', 'dev', 'ksDeviceType') or ""
        self.modelId=uci.get('paws', 'dev', 'modelId') or ""

    def set_param(self, _serialNumber, _ksDeviceEmissionPower, _ksCertId, _ksDeviceType, _modelId):
        self.serialNumber=_serialNumber
        self.ksDeviceEmissionPower=int(_ksDeviceEmissionPower)
        self.ksCertId=_ksCertId
        self.ksDeviceType=_ksDeviceType
        self.modelId=_modelId

    def to_dict(self):
        return {
            "serialNumber": self.serialNumber,
            "ksDeviceEmissionPower": self.ksDeviceEmissionPower,
            "ksCertId": self.ksCertId,
            "ksDeviceType": self.ksDeviceType,
            "modelId": self.modelId
        }
    def __str__(self):
        return "<deviceDesc: serialNumber=%s, ksDeviceEmissionPower %s ksCertId %s ksDeviceType %s modelId %s>" % (self.serialNumber, str(self.ksDeviceEmissionPower), self.ksCertId, self.ksDeviceType, self.modelId)

class location:
    def __init__(self):
        self.latitude = 37.4805
        self.longitude = 126.88381
    
    def uci_load(self, uci):
        try:
            lat = uci.get('paws', 'dev', 'geo_lati')
            lon = uci.get('paws', 'dev', 'geo_long')

            # None 체크
            if lat is None or lon is None:
                return False

            # 문자열 → float 변환
            lat = float(lat)
            lon = float(lon)

            # 범위 체크
            if not (-90.0 <= lat <= 90.0):
                return False

            if not (-180.0 <= lon <= 180.0):
                return False

            # 정상일 때만 저장
            self.latitude = lat
            self.longitude = lon

            return True

        except Exception as e:
            write_log("location uci_load error:: %s" % e)
            return False

    def set_param(self, _lat, _lon):
        try:
            lat = _lat
            lon = _lon

            # None 체크
            if lat is None or lon is None:
                return False

            # 문자열 → float 변환
            lat = float(lat)
            lon = float(lon)

            # 범위 체크
            if not (-90.0 <= lat <= 90.0):
                return False

            if not (-180.0 <= lon <= 180.0):
                return False

            # 정상일 때만 저장
            self.latitude = lat
            self.longitude = lon

            return True

        except Exception as e:
            write_log("location uci_load error:: %s" % e)
            return False
        
    def to_dict(self):
        return {
                "point": {
                    "center": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    }
                }
            }
    def __str__(self):
        return "<location: latitude=%s, longitude %s >" % (str(self.latitude), str(self.longitude))

class deviceOwner:
    def __init__(self):
        self.operator_tel = "+82 851 3872"
        self.adr_country = "KR"
        self.adr_region = "South Korea"
        self.adr_code = "08511"
        self.adr_street = "Beotkkot-ro"
        self.adr_locality = "Geumcheon-gu"
        self.operator_email = "info@nzia.kr"
        self.operator_fn = "NZIA"
        self.owner_kind = "co"
        self.owner_fn = "NZIA"
    
    def uci_load(self, uci):
        self.operator_tel = uci.get('paws', 'owner', 'operator_tel') or ""
        self.adr_country = uci.get('paws', 'owner', 'adr_country') or ""
        self.adr_region = uci.get('paws', 'owner', 'adr_region') or ""
        self.adr_code = uci.get('paws', 'owner', 'adr_code') or ""
        self.adr_street = uci.get('paws', 'owner', 'adr_street') or ""
        self.adr_locality = uci.get('paws', 'owner', 'adr_locality') or ""
        self.operator_email = uci.get('paws', 'owner', 'operator_email') or ""
        self.operator_fn = uci.get('paws', 'owner', 'operator_fn') or ""
        self.owner_kind = uci.get('paws', 'owner', 'owner_kind') or ""
        self.owner_fn = uci.get('paws', 'owner', 'owner_fn') or ""

    def set_param(self, _operator_tel, _adr_country, _adr_region, _adr_code, _adr_street, _adr_locality, _operator_email, _operator_fn, _owner_kind, _owner_fn):
        self.operator_tel = _operator_tel
        self.adr_country = _adr_country
        self.adr_region = _adr_region
        self.adr_code = _adr_code
        self.adr_street = _adr_street
        self.adr_locality = _adr_locality
        self.operator_email = _operator_email
        self.operator_fn = _operator_fn
        self.owner_kind = _owner_kind
        self.owner_fn = _owner_fn

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

    def __str__(self):
        return "<deviceOwner: operator_tel=%s, operator_fn %s >" % (self.operator_tel, self.operator_fn)

class antennaCharacteristics:
    def __init__(self):
        self.heightType="AGL"
        self.height=11.0
    
    def uci_load(self, uci):
        self.heightType=uci.get('paws', 'dev', 'ant_heightType') or ""
        self.height = float(uci.get('paws', 'dev', 'ant_height') or 0)

    def set_param(self, _heightType, _height):
        self.heightType=_heightType
        self.height=float(_height)

    def to_dict(self):
        return  {
                "heightType": self.heightType,
                "height": self.height
            }

    def __str__(self):
        return "<antennaCharacteristics: heightType=%s, height %s >" % (self.heightType, self.height)

class masterDeviceDesc:
    def __init__(self):
        self.serialNumber="WS20-224-0000004"
        self.ksDeviceEmissionPower=20
        self.ksCertId="R-R-nZc-NZC-WS20"
        self.ksDeviceType="Portable Master"
        self.modelId="NZC-WS20"
        
    
    def uci_load(self, uci):
        self.serialNumber=uci.get('paws', 'dev', 'serialNumber') or ""
        self.ksDeviceEmissionPower = int(uci.get('paws', 'dev', 'ksDeviceEmissionPower') or 0)
        self.ksCertId=uci.get('paws', 'dev', 'ksCertId') or ""
        self.ksDeviceType=uci.get('paws', 'dev', 'ksDeviceType') or ""
        self.modelId=uci.get('paws', 'dev', 'modelId') or ""

    def set_param(self, _serialNumber, _ksDeviceEmissionPower, _ksCertId, _ksDeviceType, _modelId):
        self.serialNumber=_serialNumber
        self.ksDeviceEmissionPower=int(_ksDeviceEmissionPower)
        self.ksCertId=_ksCertId
        self.ksDeviceType=_ksDeviceType
        self.modelId=_modelId

    def to_dict(self):
        return  {
                "serialNumber": self.serialNumber,
                "ksDeviceEmissionPower": self.ksDeviceEmissionPower,
                "ksCertId": self.ksCertId,
                "ksDeviceType": self.ksDeviceType,
                "modelId": self.modelId
            }

    def __str__(self):
        return "<masterDeviceDesc: serialNumber=%s, ksDeviceEmissionPower %s ksCertId %s ksDeviceType %s modelId %s>" % (self.serialNumber, str(self.ksDeviceEmissionPower), self.ksCertId, self.ksDeviceType, self.modelId)

class masterDeviceLocation:
    def __init__(self):
        self.latitude = 37.586
        self.longitude = 126.8172
    
    def uci_load(self, uci):
        lat = float(uci.get('paws', 'dev', 'geo_lati') or 0)
        lon = float(uci.get('paws', 'dev', 'geo_long') or 0)

        self.latitude = lat
        self.longitude = lon

    def set_param(self, _latitude, _longitude):
        self.latitude = float(_latitude)
        self.longitude = float(_longitude)

    def to_dict(self):
        return {
                "point": {
                    "center": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    }
                }
            }

    def __str__(self):
        return "<masterDeviceLocation: latitude=%s, longitude %s >" % (str(self.latitude), str(self.longitude))

class spectra:
    def __init__(self):
        self.bandwidth=6
        self.frequencyRanges=[]
        frequencyRanges_0={}
        frequencyRanges_0["startHz"] = 0
        frequencyRanges_0["stopHz"] = 0
        frequencyRanges_0["channelId"] = 0
        self.frequencyRanges.append(frequencyRanges_0)

    def uci_update(self, uci):
        uci.set('paws', 'ch', 'current', str(self.frequencyRanges[0]["channelId"]))

    def init_channelinfo(self):
        self.bandwidth = 6
        self.frequencyRanges[0]["startHz"] = 0
        self.frequencyRanges[0]["stopHz"] = 0
        self.frequencyRanges[0]["channelId"] = 0

    @staticmethod
    def uci_init(uci):
        uci.set('paws', 'ch', 'current', '0')

    def set_channelinfo(self, channel):
        self.bandwidth = int(channel.bandwidth)
        self.frequencyRanges[0]["startHz"] = int(channel.start_hz)
        self.frequencyRanges[0]["stopHz"] = int(channel.stop_hz)
        self.frequencyRanges[0]["channelId"] = int(channel.channel_id)

    def to_dict(self):
        return  {
                "bandwidth": self.bandwidth,
                "frequencyRanges": self.frequencyRanges
            }

    def __str__(self):
        return "<masterDeviceLocation: bandwidth=%s, startHz %s stopHz %s channelId %s>" % (str(self.bandwidth), str(self.frequencyRanges[0]["startHz"]) , str(self.frequencyRanges[0]["stopHz"]) , str(self.frequencyRanges[0]["channelId"]) )
