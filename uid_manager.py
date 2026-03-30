#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

DEVICE = "/dev/mmcblk1p6"


########################################
# 1. RAW config 전체 읽기
########################################
def read_all_config(device=DEVICE):
    cfg = {}
    s = ""
    end = 0

    f = open(device, 'rb')

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
# 2. 전체 저장 (한 번에 write)
########################################
def write_all_config(cfg, device=DEVICE):
    f = open(device, 'r+b')
    f.seek(0)

    data = ""

    for n, v in cfg.items():
        if n and v:
            data += n + "=" + v + '\0'

    data += '\0'

    f.write(data)
    f.close()


########################################
# 3. 입력 루프 (빈값 방지)
########################################
def input_loop(prompt):
    while True:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        value = sys.stdin.readline().strip()

        if value:
            return value

        print "Invalid input. Please try again."


########################################
# 4. 메인
########################################
def main():
    print "=============="

    # 기존 config 읽기
    cfg = read_all_config()

    # 필요한 항목
    keys = [
        ("serialnum", "Please input serial number: "),
        ("nct11af_mode", "Please input operation mode[ap|sta]: "),
        ("nct11af0_module", "Please input nct11af0 module type[hpa]: "),
        ("nct11af1_module", "Please input nct11af1 module type[tn]: "),
    ]

    updated = False

    # 없는 값만 입력
    for name, prompt in keys:
        if not cfg.get(name):
            cfg[name] = input_loop(prompt)
            updated = True

    # 한 번만 저장
    if updated:
        write_all_config(cfg)

    print "=============="
    print "Report"
    print "  Serial number        : %s" % cfg.get("serialnum", "")
    print "  Operation mode       : %s" % cfg.get("nct11af_mode", "")
    print "  Nct11af0 module type : %s" % cfg.get("nct11af0_module", "")
    print "  Nct11af1 module type : %s" % cfg.get("nct11af1_module", "")


if __name__ == "__main__":
    main()
