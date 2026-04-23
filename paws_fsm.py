# paws_fsm.py
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from spectrumdb.models import *
from spectrumdb.req_models import *
from uciapp_manager import UCIReader
from slave.slave_device import *
from log import write_log
RUN_TIME = 10
WAITRETRY_TIME = 300

class PawsFSM(object):
    def __init__(self, device, uci):
        self.channel_id=0
        self.device = device
        self.state = "UCIINIT"
        self.uci = uci
        self.select = "auto"
        self.lati = '0'
        self.long = "0"
        self.slavedevices = None
        self.next_state = "NONE"
        self.monitor = DeviceMonitor()

    def run(self):
        while True:
            # -----------------
            # UCIINIT
            # -----------------
            if self.state == "UCIINIT":
                write_log("STATE: UCIINIT")
                self.device._spectra.init_channelinfo()
                spectra.uci_init(self.uci)
                AvailableSpectrumResponse.uci_init(self.uci)
                self.state = "UCILOAD"
            # -----------------
            # UCILOAD
            # -----------------
            elif self.state == "UCILOAD":
                write_log("STATE: UCILOAD")
                self.select = self.uci.get('paws', 'ch', 'select')
                self.channel_id = self.uci.get('paws', 'ch', 'current')
                if isinstance(self.channel_id, basestring):
                    self.channel_id = int(self.channel_id)
                self.lati = self.uci.get('paws', 'global', 'lati')
                self.long = self.uci.get('paws', 'global', 'long')
                self.device.uci_load(self.uci)
                if self.device.blocationcheck:
                    self.state = "INIT"
                else:
                    write_log("UCILOAD location data Failed !!")
                    self.state = "WAITRETRY"
            # -----------------
            # WAITRETRY
            # -----------------
            elif self.state == "WAITRETRY":
                write_log("STATE: WAITRETRY")
                loop = 0
                looptime = RUN_TIME
                while True:
                    _retrytime = WAITRETRY_TIME
                    if(loop < _retrytime):
                        write_log("retrytime - real %s setting %s " % (str(loop), str(_retrytime)))
                        loop = loop + looptime
                        time.sleep(looptime)
                    else:
                        break
                self.state = "UCIINIT"
                
            # -----------------
            # INIT
            # -----------------
            elif self.state == "INIT":
                write_log("STATE: INIT")
                self.device.init_resp = None
                self.device.register_resp = None
                self.device.available_resp = None
                self.device.availablebatch_resp = None
                self.device.notify_resp = None
                self.device.channel = None
                self.device.expire_time=None
                try:
                    self.device.init_resp = self.device.db.init_req(self.device)
                    if isinstance(self.device.init_resp, InitResponse):
                        write_log(self.device.init_resp)
                        self.state = "REGISTER"
                    else:
                        write_log("INIT Failed")
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("INIT ERROR: %s" % str(e))
                    self.state = "WAITRETRY"
            # -----------------
            # REGISTER
            # -----------------
            elif self.state == "REGISTER":
                write_log("STATE: REGISTER")
                self.device.register_resp = None
                try:
                    self.device.register_resp = self.device.db.register_req(self.device)
                    if isinstance(self.device.register_resp, RegisterResponse):
                        write_log(self.device.register_resp)
                        self.state = "AVAILABLE"
                    else:
                        write_log("REGISTER Failed")
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("REGISTER ERROR: %s" % str(e))
                    self.state = "WAITRETRY"
            # -----------------
            # AVAILABLE
            # -----------------
            elif self.state == "AVAILABLE":
                write_log("STATE: AVAILABLE")
                self.device.available_resp = None
                try:
                    self.device.available_resp = self.device.db.avail_req(self.device)
                    if isinstance(self.device.available_resp, AvailableSpectrumResponse):
                        write_log(self.device.available_resp)
                        size = len(self.device.available_resp.profiles)
                        if size > 0:
                            if self.select == 'auto':
                                _Channel = self.device.available_resp.profiles[0]
                                self.uci.set('paws', 'ch', 'current', str(_Channel.channel_id))
                                write_log("AVAILABLE -> USENOTIFY")
                                self.state = "USENOTIFY"
                            else:
                                self.state = "UCIUPDATE"
                        else:
                            write_log("AVAILABLE Not channel")
                            self.state = "OPERATE"
                    else:
                        write_log("AVAILABLE Failed")
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("AVAILABLE ERROR: %s" % str(e))
                    self.state = "WAITRETRY"
            # -----------------
            # AVAILABLE BATCH
            # -----------------
            elif self.state == "AVAILABLEBATCH":
                write_log("STATE: AVAILABLEBATCH")
                self.device.availablebatch_resp = None
                try:
                    self.device.availablebatch_resp = self.device.db.availbatch_req(self.device)
                    if isinstance(self.device.availablebatch_resp, AvailableBatchSpectrumResponse):
                        write_log(self.device.availablebatch_resp)
                        size = len(self.device.availablebatch_resp.profiles)
                        if size > 0:
                            if self.select == 'auto':
                                self.state = "USENOTIFY"
                            else:
                                self.state = "UCIUPDATE"
                        else:
                            write_log("AVAILABLEBATCH Not channel")
                            self.state = "WAITRETRY"
                    else:
                        write_log("AVAILABLEBATCH Failed")
                        self.state = "WAITRETRY"
                except Exception as e:
                    write_log("AVAILABLEBATCH ERROR: %s" % str(e))
                    self.state = "WAITRETRY"
                
            # -----------------
            # USENOTIFY
            # -----------------
            elif self.state == "USENOTIFY":
                write_log("STATE: USENOTIFY")
                self.device.notify_resp = None
                self.device.expire_time=None
                bnotify = False
                if self.device.available_resp and len(self.device.available_resp.profiles)>0:
                    try:
                        _current = self.uci.get('paws', 'ch', 'current')
                        if isinstance(_current, basestring):
                            _current = int(_current)
                        if _current >= 14 and _current <= 51:
                            self.device.channel = self.device.available_resp.get_Channel(_current)
                            if self.device.channel != None:
                                self.device._spectra.set_channelinfo(self.device.channel)

                                self.device.notify_resp = self.device.db.notify_req(self.device)
                                if isinstance(self.device.notify_resp, NotifyResponse):
                                    write_log(self.device.notify_resp)
                                    self.device.expire_time=self.device.notify_resp.select_channel.stopTime
                                    self.channel_id=self.device.notify_resp.select_channel.channel_id
                                    if isinstance(self.channel_id, basestring):
                                        self.channel_id = int(self.channel_id)
                                    bnotify = True
                                    self.state = "UCIUPDATE"
                                else:
                                    write_log("USENOTIFY Instance Failed")
                            else:
                                write_log("get Channel class - channel_id %s select Failed" % (str(_current)))
                        else:
                            write_log("Channel Arear Failed")
                    except Exception as e:
                        write_log("USENOTIFY ERROR: %s " % str(e))
                else:
                    write_log("USENOTIFY ERROR: USE NOT CHANNEL !!")
                    self.state = "OPERATE"
                if bnotify == False:
                    self.uci.set('paws', 'ch', 'current', '0')
                    self.channel_id = 0
                    self.state = "OPERATE"

            # -----------------
            # UCIUPDATE
            # -----------------
            elif self.state == "UCIUPDATE":
                write_log("STATE: UCIUPDATE")
                self.device.uci_update(self.uci)
                lines = UCIReader.show_and_filter('paws')
                for line in lines:
                    write_log(line)
                self.state = "OPERATE"
            # -----------------
            # OPERATE
            # -----------------
            elif self.state == "OPERATE":
                write_log("STATE: OPERATE")
                _testmode = self.uci.get('paws', 'global', 'testmode')
                if _testmode == 'y':
                    self.uci.set('paws', 'global', 'testmode', 'n')
                    write_log("testmode - paws again!!")
                    self.state = "UCIINIT"
                else:
                    _current = self.uci.get('paws', 'ch', 'current')
                    _lati = self.uci.get('paws', 'global', 'lati')
                    _long = self.uci.get('paws', 'global', 'long')
                    if isinstance(_current, basestring):
                        _current = int(_current)
                        write_log("current channel: %s" % str(_current))
                    write_log("OPERATE -> lati : uci %s cur %s" % (str(_lati), str(self.lati)))
                    write_log("OPERATE -> long : uci %s cur %s" % (str(_long), str(self.long)))
                    write_log("OPERATE -> channel_id : uci %s cur %s" % (str(_current), str(self.channel_id)))
                    if _lati != self.lati and _long != self.long:
                        self.state = "UCIINIT"
                    elif (_current>=14 and _current<=51) and _current != self.channel_id:
                        self.state = "USENOTIFY"
                    else:
                        if self._is_expired():
                            write_log("Spectrum expired request again")
                            self.state = "UCIINIT"
                        else:
                            self.monitor.slave_fetch()
                            if self.monitor.bchanged:
                                self.monitor.bchanged = False
                                self.state = "SLAVEPAWS"
                        time.sleep(RUN_TIME)

            # -----------------
            # SLAVEPAWS AVAILABLE + USENOTIFY
            # -----------------
            elif self.state == "SLAVEPAWS":
                write_log("STATE: SLAVEPAWS")
                self.monitor.slave_fetch()
                slavedevices = self.monitor.get_slavedevice() or {}
                for serial, slavedev in slavedevices.items():
                    write_log("DEVICE: %s" % str(serial))
                    if slavedev.pawsnew == 0:
                        continue
                    else:
                        slavedev.pawsnew = 0
                    try:
                        desc, loc, ant = slavedev.to_req_models()
                        write_log("STATE: SLAVE AVAILABLE")
                        slavedev_available_resp = self.device.db.slaveavail_req(self.device, desc, loc, ant)
                        if isinstance(slavedev_available_resp, AvailableSpectrumResponse):
                            write_log(slavedev_available_resp)
                            size = len(slavedev_available_resp.profiles)
                            if size > 0 and (self.channel_id >= 14 and self.channel_id <= 51):
                                slave_channel = slavedev_available_resp.get_Channel(self.channel_id)
                                if slave_channel != None:
                                    slave_spectra = spectra()
                                    slave_spectra.set_channelinfo(slave_channel)
                                    write_log("STATE: SLAVE USENOTIFY")
                                    slavedev_notify_resp = self.device.db.slavenotify_req(self.device, desc, loc, ant, slave_spectra)
                                    if isinstance(slavedev_notify_resp, NotifyResponse):
                                        slavedev.channel_id = self.channel_id
                                        self.monitor.ubus_devicechannel(slavedev.serial, slavedev.channel_id, slavedev.pawsnew)
                                        write_log(slavedev_notify_resp)
                                    else:
                                        write_log("Slave USENOTIFY Instance Failed")
                                else:
                                    write_log("Slave Find Channel Class Failed : master channel id %s " % (str(self.channel_id)))
                            else:
                                write_log("Slave AVAILABLESPECTRUM Instance Failed")
                    except Exception as e:
                        write_log("Slave Device processing error: %s" % str(e))
                
                self.state = "OPERATE"
    # -----------------
    # expire check
    # -----------------
    def _is_expired(self):
        if not self.device.expire_time:
            return False

        expire = datetime.strptime(
            self.device.expire_time,
            "%Y-%m-%d %H:%M:%S"
        )

        now = datetime.utcnow()
        remaining = (expire - now).total_seconds()

        # 로그 출력 (초 단위)
        write_log("[DEBUG] expire remaining: {:.2f} seconds".format(remaining))

        return now >= expire
