# spectrumdb_client.py
# -*- coding: utf-8 -*-

import json
import urllib2
from spectrumdb_response import SpectrumDBResponseParser

# 유니코드 딕셔너리를 utf-8 딕셔너리로 변환하는 함수
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class SpectrumDB(object):
    def __init__(self, server_url):
        self.server_url = server_url
        self.headers = {
            "Content-Type": "application/json"
        }

    def _post(self, method, payload):
        body = {
            "jsonrpc": "2.0",
            "method": method,
            "params": payload,
            "id": "000001"
        }
        data = json.dumps(body)
        print(data)
        req = urllib2.Request(
            self.server_url,
            data,
            self.headers
        )
        response = urllib2.urlopen(req)
        resp_json = byteify(json.loads(response.read()))
        print(resp_json)

        if "result" in resp_json:
            return resp_json["result"]
        raise Exception("PAWS DB Error: %s" % resp_json)

    # -------------------------
    # INIT
    # -------------------------

    def init_req(self, config):
        payload = {
                "version": "1.0",
                "type": "INIT_REQ",
                "deviceDesc": {
                    "serialNumber": "WS20-224-0000004",
                    "ksDeviceEmissionPower": 20,
                    "ksCertId": "R-R-nZc-NZC-WS20",
                    "ksDeviceType": "Portable Master",
                    "modelId": "NZC-WS20"
                },
                "location": {
                    "point": {
                        "center": {
                            "latitude": 37.586,
                            "longitude": 126.8172
                        }
                    }
                }
            }
        resp = self._post(
            "spectrum.paws.init",
            payload
        )
        print(resp)
        return SpectrumDBResponseParser.parse_init(resp)

    # -------------------------
    # REGISTER
    # -------------------------
# {
#     "method": "spectrum.paws.register",
#     "id": "000002",
#     "params": {
#         "version": "1.0",
#         "type": "REGISTRATION_REQ",
#         "deviceDesc": {
#             "serialNumber": "WS20-224-0000004",
#             "ksDeviceEmissionPower": 20,
#             "ksCertId": "R-R-nZc-NZC-WS20",
#             "ksDeviceType": "Portable Master",
#             "modelId": "NZC-WS20"
#         },
#         "location": {
#             "point": {
#                 "center": {
#                     "latitude": 37.586,
#                     "longitude": 126.8172
#                 }
#             }
#         },
#         "deviceOwner": {
#             "operator": {
#                 "tel": "+82 32 650 5766",
#                 "adr": {
#                     "country": "KR",
#                     "region": "South Korea",
#                     "code": "21315",
#                     "street": "bupyungdearo 293",
#                     "locality": "bupyunggu"
#                 },
#                 "email": "welcome@nzia.kr",
#                 "fn": "NZIA"
#             },
#             "owner": {
#                 "kind": "co",
#                 "fn": "NZIA"
#             }
#         },
#         "antennaCharacteristics": {
#             "heightType": "AGL",
#             "height": 11.0
#         }
#     }
# }
    def register_req(self, config):
        payload = {
            "deviceDesc": config["deviceDesc"],
            "location": config["location"],
            "antenna": config["antenna"],
            "owner": config["owner"]
        }
        resp = self._post(
            "spectrum.paws.register",
            payload
        )
        return SpectrumDBResponseParser.parse_register(resp)

    # -------------------------
    # AVAILABLE
    # -------------------------

    def avail_req(self, config):
        payload = {
            "deviceDesc": config["deviceDesc"],
            "location": config["location"]
        }
        resp = self._post(
            "spectrum.paws.getSpectrum",
            payload
        )
        return SpectrumDBResponseParser.parse_available(resp)
