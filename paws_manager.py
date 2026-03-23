# paws_manager.py
# -*- coding: utf-8 -*-

from spectrumdb.spectrumdb_client import SpectrumDB
from bs import BS
from cpe import CPE
from paws_fsm import PawsFSM
from uciapp_manager import UCIReader
from bshttpserver import start_server_thread, setup_signal

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
    # windows
    uci = UCIReader(uci_dir='.\\config')
    # linux openwrt
    # uci = UCIReader(uci_dir='/etc/config')
    _devicetype = uci.get('paws', 'dev', 'ksDeviceType')
    _serverurl = uci.get('paws', 'global', 'serverurl')
    if _devicetype == "Portable Master" or _devicetype == "Fixed Master":
        db = SpectrumDB(_serverurl)
        device = BS(CONFIG, db)

        # 서버 먼저 실행 (thread)
        start_server_thread(device, uci)
        # 시그널 등록
        setup_signal()
        # FSM 실행 (block)
        fsm = PawsFSM(device, uci)
        fsm.run()
    else:
        device = CPE(CONFIG)
        device.run()
if __name__ == "__main__":
    main()
