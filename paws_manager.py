# paws_manager.py
# -*- coding: utf-8 -*-

from spectrumdb.spectrumdb_client import SpectrumDB
from bs import BS
from cpe import CPE
from paws_fsm import PawsFSM
from uciapp_manager import UCIReader
from log import write_log

def main():
    # windows
    uci = UCIReader(uci_dir='.\\config')
    # linux openwrt
    # uci = UCIReader(uci_dir='/etc/config')
    _use = uci.get('paws', 'global', 'use')
    if _use == 'y':
        _ksDeviceType = uci.get('system', 'dev', 'deviceType')
        _serverurl = uci.get('paws', 'global', 'serverurl')
        if _ksDeviceType == "Portable Master" or _ksDeviceType == "Fixed Master":
            db = SpectrumDB(_serverurl)
            device = BS(_ksDeviceType, db)
            fsm = PawsFSM(device, uci)
            fsm.run()
        else:
            device = CPE(_ksDeviceType, uci)
            device.run()
    else:
        write_log("paws process end!")
if __name__ == "__main__":
    main()
