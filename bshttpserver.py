# bshttpserver.py
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import signal
import sys

httpd = None

CPE_REQ = {
    "type": "AVAIL_SPEC_REQ",
    "deviceDesc": {
        "serialNumber": "WS20-224-0000004", 
        "ksDeviceEmissionPower": 20, 
        "ksCertId": "R-R-nZc-NZC-WS20", 
        "ksDeviceType": "Fixed Slave", 
        "modelId": "NZC-WS20"
    }, 
    "location": {
        "point": {
            "center": {
                "latitude": 37.586, 
                "longitude": 126.8172
            }
        }
    },
    "antennaCharacteristics": {
        "heightType": "AGL",
        "height": 11.0
    },
    "spectra": {
        "bandwidth": 6,
        "frequencyRanges": [
            {
                "startHz": 536,
                "stopHz": 542,
                "channelId": 25
            }
        ]
    }
}


class BSHttpServer(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_error(400)
            return

        body = self.rfile.read(content_length)

        try:
            req = json.loads(body.decode('utf-8'))
        except:
            self.send_error(400)
            return

        print("BODY:", body)
        print("REQ:", req)

        # device, uci 가져오기 (핵심)
        device = self.server.device
        uci = self.server.uci

        req_type = req.get("type")

        if req_type == "AVAIL_SPEC_REQ":
            print("type : AVAIL_SPEC_REQ")
            _deviceDesc = req.get("deviceDesc")
            _location = req.get("location")
            _antennaCharacteristics = req.get("antennaCharacteristics")
            resp = device.db.availnet_req(device, _deviceDesc, _location, _antennaCharacteristics)
            print(resp)

        elif req_type == "SPECTRUM_USE":
            print("type : SPECTRUM_USE")
            resp = {
                "type": "AVAILABLE_SPECTRUM_RESP",
                "channels": channels,
                "maxPower": 30
            }

        else:
            resp = {"type": "ERROR", "message": "Unknown request"}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(resp).encode('utf-8'))


# -----------------------------
# 서버 실행 함수
# -----------------------------
def run_server(device, uci):
    global httpd

    HTTPServer.allow_reuse_address = True

    httpd = HTTPServer(('0.0.0.0', 8080), BSHttpServer)

    # device / uci 주입
    httpd.device = device
    httpd.uci = uci

    print("BS HTTP Server Started")
    httpd.serve_forever()


# -----------------------------
# 스레드로 실행
# -----------------------------
def start_server_thread(device, uci):
    t = threading.Thread(target=run_server, args=(device, uci))
    t.daemon = True
    t.start()
    return t


# -----------------------------
# 종료 처리 (메인 스레드에서만)
# -----------------------------
def signal_handler(sig, frame):
    global httpd
    print("Shutting down server...")

    if httpd:
        httpd.shutdown()

    sys.exit(0)


def setup_signal():
    # 메인 스레드에서만 등록
    if threading.current_thread().name == "MainThread":
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
