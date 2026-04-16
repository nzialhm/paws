import json
from typing import List
import subprocess


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
    def from_dict(cls, data: dict):
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
        return f"<Device serial={self.serial} ip={self.ip}>"



class DevicesResponse:
    def __init__(self, devices: List[Device]):
        self.devices = devices

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        devices = [Device.from_dict(d) for d in data.get("devices", [])]
        return cls(devices)

    def get_by_serial(self, serial: str):
        for d in self.devices:
            if d.serial == serial:
                return d
        return None

    def __repr__(self):
        return f"<DevicesResponse count={len(self.devices)}>"
    


if __name__ == "__main__":
    # ubus 호출
    result = subprocess.check_output(
        ["ubus", "call", "system_manager", "devices"]
    )

    json_str = result.decode()

    # 파싱
    devices_resp = DevicesResponse.from_json(json_str)

    print(devices_resp)

    for d in devices_resp.devices:
        print(d.serial, d.ip)
