#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import select

DEVICE = "/dev/mmcblk1p6"


########################################
# 콘솔 자동 감지
########################################
def get_console():
    try:
        with open("/proc/cmdline", "r") as f:
            cmd = f.read()

        for item in cmd.split():
            if item.startswith("console="):
                cons = item.split("=")[1].split(",")[0]
                return "/dev/" + cons
    except:
        pass

    # fallback 후보들
    for dev in ["/dev/ttyS0", "/dev/ttymxc0", "/dev/ttyAMA0"]:
        if os.path.exists(dev):
            return dev

    return None


TTY_PATH = get_console()


########################################
# tty open
########################################
try:
    tty = open(TTY_PATH, "r+", buffering=1) if TTY_PATH else None
except:
    tty = None


########################################
# 출력
########################################
def log_print(msg):
    # stdout
    try:
        sys.stdout.write(msg + "\n")
        sys.stdout.flush()
    except:
        pass

    # tty
    if tty:
        try:
            tty.write(msg + "\n")
            tty.flush()
        except:
            pass


########################################
# 입력 (timeout 기반)
########################################
def safe_input(prompt, timeout=10):
    if not tty:
        return None

    try:
        log_print(prompt)

        tty.write(prompt)
        tty.flush()

        rlist, _, _ = select.select([tty], [], [], timeout)

        if rlist:
            value = tty.readline().strip()
            return value
        else:
            log_print("[TIMEOUT] No input")
            return None

    except:
        return None


########################################
# 입력 루프
########################################
def input_loop(prompt, default=None):
    value = safe_input(prompt)

    if not value:
        log_print("[INFO] Using default: %s" % default)
        return default

    return value


########################################
# RAW config 읽기
########################################
def read_all_config(device=DEVICE):
    cfg = {}
    s = ""
    end = 0

    try:
        f = open(device, 'rb')
    except:
        log_print("[ERROR] Cannot open device")
        return cfg

    while True:
        c = f.read(1)
        if not c:
            break

        if ord(c) < ord(' '):
            end += 1
            if s:
                parts = s.split("=", 1)
                if len(parts) > 1:
                    cfg[parts[0]] = parts[1]
            s = ""

            if end > 1:
                break
        else:
            end = 0
            s += c

    f.close()
    return cfg


########################################
# 저장
########################################
def write_all_config(cfg, device=DEVICE):
    try:
        f = open(device, 'r+b')
    except:
        log_print("[ERROR] Cannot write device")
        return

    f.seek(0)

    data = ""
    for n, v in cfg.items():
        if n and v:
            data += n + "=" + v + '\0'

    data += '\0'

    f.write(data)
    f.close()


########################################
# 메인
########################################
def main():
    log_print("==============")
    log_print("Using console: %s" % str(TTY_PATH))

    cfg = read_all_config()

    keys = [
        ("serialnum", "Please input serial number: ", "UNKNOWN"),
        ("nct11af_mode", "Please input operation mode[ap|sta]: ", "ap"),
        ("nct11af0_module", "Please input nct11af0 module type[hpa]: ", "hpa"),
        ("nct11af1_module", "Please input nct11af1 module type[tn]: ", "tn"),
    ]

    updated = False

    for name, prompt, default in keys:
        if not cfg.get(name):
            cfg[name] = input_loop(prompt, default)
            updated = True

    if updated:
        write_all_config(cfg)

    log_print("==============")
    log_print("Report")
    log_print("  Serial number        : %s" % cfg.get("serialnum", ""))
    log_print("  Operation mode       : %s" % cfg.get("nct11af_mode", ""))
    log_print("  Nct11af0 module type : %s" % cfg.get("nct11af0_module", ""))
    log_print("  Nct11af1 module type : %s" % cfg.get("nct11af1_module", ""))


if __name__ == "__main__":
    main()
