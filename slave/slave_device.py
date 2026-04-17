# slave_device.py
# -*- coding: utf-8 -*-
import json
import subprocess
import time


class Device:
    def __init__(self, serial, model, cert_id, dev_type,
                 ip, lat, lon, height_type, height):
        self.serial = serial
        self.model = model
        self.cert_id = cert_id
        self.type = dev_type
        self.ip = ip
        self.lat = lat
        self.lon = lon
        self.height_type = height_type
        self.height = height

    @classmethod
    def from_dict(cls, data):
        return cls(
            serial=data.get("serial", ""),
            model=data.get("model", ""),
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

        # 신규 device
        for serial in _slaves:
            if serial not in prev:
                self.bchanged = True
                print("[NEW] %s (%s)" % (serial, _slaves[serial].ip))

        # 삭제된 device
        for serial in prev:
            if serial not in _slaves:
                self.bchanged = True
                print("[REMOVED] %s (%s)" % (serial, _slaves[serial].ip))

        # 변경 감지 (lat lon 기준 예시)
        for serial in _slaves:
            if serial in prev:
                old = prev[serial]
                new = _slaves[serial]

                if old.lat != new.lat:
                    self.bchanged = True
                    print("[CHANGED] %s lot %s -> %s" %
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

    def run(self):
        print("[START] Device monitor running...")

        while True:
            slaves = self.fetch_devices()

            if slaves is not None:
                self.detect_changes(slaves)
                self.current_devices = slaves

            time.sleep(5)


# 실행
if __name__ == "__main__":
    monitor = DeviceMonitor()
    monitor.run()
