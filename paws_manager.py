# paws_manager.py
# -*- coding: utf-8 -*-

from spectrumdb.spectrumdb_client import SpectrumDB
from bs import BS
from cpe import CPE
from paws_fsm import PawsFSM
from uciapp_manager import UCIReader

def main():
    # windows
    uci = UCIReader(uci_dir='.\\config')
    # linux openwrt
    # uci = UCIReader(uci_dir='/etc/config')
    _use = uci.get('paws', 'global', 'use')
    if _use == 'y':
        _devicetype = uci.get('paws', 'dev', 'ksDeviceType')
        _serverurl = uci.get('paws', 'global', 'serverurl')
        if _devicetype == "Portable Master" or _devicetype == "Fixed Master":
            db = SpectrumDB(_serverurl)
            device = BS(_devicetype, db)
            fsm = PawsFSM(device, uci)
            fsm.run()
        else:
            device = CPE(_devicetype, uci)
            device.run()
    else:
        print("paws process end!")
if __name__ == "__main__":
    main()
