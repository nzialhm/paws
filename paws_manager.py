# paws_manager.py
# -*- coding: utf-8 -*-

from spectrumdb.spectrumdb_client import SpectrumDB
from bs import BS
from cpe import CPE
from paws_fsm import PawsFSM
from uciapp_manager import UCIReader
import traceback
from log import write_log

def main():
    # windows
    uci = UCIReader(uci_dir='.\\config')
    # linux openwrt
    # uci = UCIReader(uci_dir='/etc/config')
    _use = uci.get('paws', 'global', 'use')
    if _use == 'y':
        _mode_name = uci.get('paws', 'global', 'mode_name') or "default_nct11af1"
        _nct11af_mode = uci.get('wireless', _mode_name, 'mode')
        _nct11af_mode = str(_nct11af_mode).strip() if _nct11af_mode else ""

        _ksDeviceType = uci.get('system', 'dev', 'deviceType')
        _serverurl = uci.get('paws', 'global', 'serverurl')
        if _nct11af_mode == "ap":
            if not _serverurl:
                write_log("serverurl not configured")
                return        
            db = SpectrumDB(_serverurl)
            device = BS(_ksDeviceType, db)
            fsm = PawsFSM(device, uci)
            try:
                fsm.run()
            except Exception as e:
                write_log("FSM error: %s" % e)
                write_log(traceback.format_exc())
        else:
            device = CPE(_ksDeviceType, uci)
            try:
                device.run()
            except Exception as e:
                write_log("CPE error: %s" % e)
                write_log(traceback.format_exc())
    else:
        write_log("paws process end!")

if __name__ == "__main__":
    main()
