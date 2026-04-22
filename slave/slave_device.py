# slave_device.py
# -*- coding: utf-8 -*-
import json
import subprocess
import time
from spectrumdb.req_models import *


class Device:
    def __init__(self, serial, model_id, power, cert_id, dev_type,
                 ip, lat, lon, height_type, height):
        self.serial = serial
        self.model_id = model_id
        self.cert_id = cert_id
        self.type = dev_type
        self.ip = ip
        self.power = power
        self.lat = lat
        self.lon = lon
        self.height_type = height_type
        self.height = height

    @classmethod
    def from_dict(cls, data):
        return cls(
            serial=data.get("serial", ""),
            model_id=data.get("model", ""),
            power=data.get("power", ""),
            cert_id=data.get("cert_id", ""),
            dev_type=data.get("type", ""),
            ip=data.get("ip", ""),
            lat=data.get("lat", 0.0),
            lon=data.get("lon", 0.0),
            height_type=data.get("height_type", ""),
            height=data.get("height", 0.0),
        )

    def __repr__(self):
        return "<Device serial=%s ip=%s>" % (self.serial, self.ip)

    # 추가: req_models 변환
    def to_req_models(self):
        desc = deviceDesc()
        loc = location()
        ant = antennaCharacteristics()

        # 안전하게 타입 변환
        desc.set_param(
            self.serial,
            int(self.power) if self.power != "" else 0,
            self.cert_id,
            self.type,
            self.model_id
        )

        loc.set_param(
            float(self.lat),
            float(self.lon)
        )

        ant.set_param(
            self.height_type,
            float(self.height)
        )

        return desc, loc, ant

    # 추가: 바로 dict payload 생성
    def to_request_payload(self):
        desc, loc, ant = self.to_req_models()

        return {
            "deviceDesc": desc.to_dict(),
            "location": loc.to_dict(),
            "antennaCharacteristics": ant.to_dict()
        }


class DevicesResponse:
    def __init__(self, devices):
        self.devices = devices

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        devices = [Device.from_dict(d) for d in data.get("devices", [])]
        return cls(devices)

    def to_dict(self):
        return {d.serial: d for d in self.devices}


# 핵심: 감시 클래스
class DeviceMonitor:
    def __init__(self):
        self.current_devices = {}
        self.bchanged = False
        self.bchangnew = False
        self.bchangrm = False

    def fetch_devices(self):
        try:
            result = subprocess.check_output(
                ["ubus", "call", "system_manager", "devices"]
            )
        except subprocess.CalledProcessError as e:
            print("[ERROR] ubus call failed:", e)
            return None

        json_str = result if isinstance(result, str) else result.decode()

        try:
            resp = DevicesResponse.from_json(json_str)
            return resp.to_dict()
        except Exception as e:
            print("[ERROR] JSON parsing failed:", e)
            return None

    def detect_changes(self, _slaves):
        prev = self.current_devices

        for serial in _slaves:
            if serial not in prev:
                self.bchanged = True
                self.bchangnew = True
                print("[NEW] %s (%s)" % (serial, _slaves[serial].ip))

        for serial in prev:
            if serial not in _slaves:
                self.bchanged = True
                self.bchangrm = True
                print("[REMOVED] %s (%s)" % (serial, prev[serial].ip))

        for serial in _slaves:
            if serial in prev:
                old = prev[serial]
                new = _slaves[serial]

                if old.lat != new.lat:
                    self.bchanged = True
                    print("[CHANGED] %s lat %s -> %s" %
                          (serial, old.lat, new.lat))
                if old.lon != new.lon:
                    self.bchanged = True
                    print("[CHANGED] %s lon %s -> %s" %
                          (serial, old.lon, new.lon))

    def slave_fetch(self):
        print("[SLAVE] Device Fetch")
        slaves = self.fetch_devices()
        if slaves is not None:
            self.detect_changes(slaves)
            self.current_devices = slaves

    def get_slavedevice(self):
        return self.current_devices

    def run(self):
        print("[START] Device monitor running...")
        while True:
            self.slave_fetch()

            devices = self.get_slavedevice() or {}

            for serial, dev in devices.items():
                print("DEVICE: %s" % serial)

                try:
                    desc, loc, ant = dev.to_req_models()
                    payload = dev.to_request_payload()

                    print("===================================")
                    print("payload: %s" % repr(payload))
                    print("=====================================")
                    print("DESC: %s" % repr(desc.to_dict() if desc else None))
                    print("LOC: %s" % repr(loc.to_dict() if loc else None))
                    print("ANT: %s" % repr(ant.to_dict() if ant else None))

                except Exception as e:
                    import traceback
                    print("Device processing error: %s" % str(e))
                    print(traceback.format_exc())

            time.sleep(5)



# 실행
if __name__ == "__main__":
    monitor = DeviceMonitor()
    monitor.run()
