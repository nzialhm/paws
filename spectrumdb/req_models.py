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
        self.serialNumber=uci.get(file, 'dev', 'serialNumber')
        self.ksDeviceEmissionPower=uci.get(file, 'dev', 'ksDeviceEmissionPower')
        self.ksCertId=uci.get(file, 'dev', 'ksCertId')
        self.ksDeviceType=uci.get(file, 'dev', 'ksDeviceType')
        self.modelId=uci.get(file, 'dev', 'modelId')

    def to_dict(self):
        return {
            "serialNumber": self.serialNumber,
            "ksDeviceEmissionPower": self.ksDeviceEmissionPower,
            "ksCertId": self.ksCertId,
            "ksDeviceType": self.ksDeviceType,
            "modelId": self.modelId
        }
    def __str__(self):
        return "<deviceDesc: serialNumber=%s, ksDeviceEmissionPower %d ksCertId %s ksDeviceType %s modelId %s>" % (self.serialNumber, self.ksDeviceEmissionPower, self.ksCertId, self.ksDeviceType, self.modelId)

class location:
    def __init__(self):
        self.latitude = 37.4805
        self.longitude = 126.88381
    
    def uci_load(self, uci, file):
        try:
            lat = uci.get(file, 'dev', 'geo_lati')
            lon = uci.get(file, 'dev', 'geo_long')

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
            print("uci_load error:", e)
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
        return "<location: latitude=%d, longitude %d >" % (self.latitude, self.longitude)

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
    
    def uci_load(self, uci, file):
        self.operator_tel = uci.get(file, 'owner', 'operator_tel')
        self.adr_country = uci.get(file, 'owner', 'adr_country')
        self.adr_region = uci.get(file, 'owner', 'adr_region')
        self.adr_code = uci.get(file, 'owner', 'adr_code')
        self.adr_street = uci.get(file, 'owner', 'adr_street')
        self.adr_locality = uci.get(file, 'owner', 'adr_locality')
        self.operator_email = uci.get(file, 'owner', 'operator_email')
        self.operator_fn = uci.get(file, 'owner', 'operator_fn')
        self.owner_kind = uci.get(file, 'owner', 'owner_kind')
        self.owner_fn = uci.get(file, 'owner', 'owner_fn')

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
    
    def uci_load(self, uci, file):
        self.heightType=uci.get(file, 'dev', 'ant_heightType')
        self.height=uci.get(file, 'dev', 'ant_height')

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
        
    
    def uci_load(self, uci, file):
        self.serialNumber=uci.get(file, 'dev', 'serialNumber')
        self.ksDeviceEmissionPower=uci.get(file, 'dev', 'ksDeviceEmissionPower')
        self.ksCertId=uci.get(file, 'dev', 'ksCertId')
        self.ksDeviceType=uci.get(file, 'dev', 'ksDeviceType')
        self.modelId=uci.get(file, 'dev', 'modelId')

    def to_dict(self):
        return  {
                "serialNumber": self.serialNumber,
                "ksDeviceEmissionPower": self.ksDeviceEmissionPower,
                "ksCertId": self.ksCertId,
                "ksDeviceType": self.ksDeviceType,
                "modelId": self.modelId
            }

    def __str__(self):
        return "<masterDeviceDesc: serialNumber=%s, ksDeviceEmissionPower %d ksCertId %s ksDeviceType %s modelId %s>" % (self.serialNumber, self.ksDeviceEmissionPower, self.ksCertId, self.ksDeviceType, self.modelId)

class masterDeviceLocation:
    def __init__(self):
        self.latitude = 37.586
        self.longitude = 126.8172
    
    def uci_load(self, uci, file):
        self.latitude = uci.get(file, 'dev', 'geo_lati')
        self.longitude = uci.get(file, 'dev', 'geo_long')

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
        return "<masterDeviceLocation: latitude=%s, longitude %s >" % (self.latitude, self.longitude)

class spectra:
    def __init__(self):
        self.bandwidth=6
        self.frequencyRanges=[]
        frequencyRanges_0={}
        frequencyRanges_0["startHz"] = 0
        frequencyRanges_0["stopHz"] = 0
        frequencyRanges_0["channelId"] = 0
        self.frequencyRanges.append(frequencyRanges_0)

    def uci_update(self, uci, file):
        uci.set(file, 'ch', 'current', self.frequencyRanges[0]["channelId"])

    @staticmethod
    def uci_init(uci):
        _respfile = 'paws'
        uci.set(_respfile, 'ch', 'current', '')

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

    def __str__(self):
        return "<masterDeviceLocation: bandwidth=%d, startHz %d stopHz %d channelId %d>" % (self.bandwidth, self.frequencyRanges[0]["startHz"] , self.frequencyRanges[0]["stopHz"] , self.frequencyRanges[0]["channelId"] )
