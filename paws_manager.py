# paws_manager.py
# -*- coding: utf-8 -*-

from spectrumdb.spectrumdb_client import SpectrumDB
from bs import BS
from cpe import CPE
from paws_fsm import PawsFSM

SERVER = "https://www.tvws.kr/cmpipe/tvwsdb"
DEVICE_TYPE = "bs"
CONFIG = {
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

def main():
    if DEVICE_TYPE == "bs":
        db = SpectrumDB(SERVER)
        device = BS(CONFIG, db)
        fsm = PawsFSM(device)
        fsm.run()
    else:
        device = CPE(CONFIG)
        device.run()
if __name__ == "__main__":
    main()
