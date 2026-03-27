#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

DEVICE = "/dev/mmcblk1p6"


########################################
# 1. RAW config 읽기
########################################
def read_all_config(device=DEVICE):
    cfg = []
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
                cfg.append(parts)
            s = ""

            if end > 1:
                break
        else:
            end = 0
            s += c

    f.close()
    return cfg


########################################
# 2. 값 조회
########################################
def get_value(name, device=DEVICE):
    cfg = read_all_config(device)

    for line in cfg:
        if len(line) > 1 and line[0] == name:
            return line[1]

    return ""


########################################
# 3. 값 설정
########################################
def set_value(name, value, device=DEVICE):
    cfg = read_all_config(device)

    new_cfg = []
    found = 0

    for line in cfg:
        if len(line) > 1:
            n = line[0]
            v = line[1]

            if n == name:
                found = 1
                if value != "":
                    new_cfg.append((name, value))
            else:
                if n != "" and v != "":
                    new_cfg.append((n, v))

    if found == 0 and value != "":
        new_cfg.append((name, value))

    f = open(device, 'r+b')
    f.seek(0)

    data = ""

    for n, v in new_cfg:
        data += n + "=" + v + '\0'

    data += '\0'

    f.write(data)
    f.close()


########################################
# 4. 입력 루프
########################################
def input_loop(prompt):
    while True:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        value = sys.stdin.readline().strip()

        if value != "":
            return value

        print "Invalid input. Please try again."


########################################
# 5. 값 보장 (없으면 입력받고 저장)
########################################
def ensure_value(name, prompt):
    value = get_value(name)

    while value == "":
        value = input_loop(prompt)
        set_value(name, value)

        # 저장 확인
        value = get_value(name)

    return value


########################################
# 6. 메인 (내부 로직만 실행)
########################################
def main():
    print "=============="

    serial = ensure_value("serialnum", "Please input serial number: ")
    mode = ensure_value("nct11af_mode", "Please input operation mode[ap|sta]: ")
    mod0 = ensure_value("nct11af0_module", "Please input nct11af0 module type[hpa]: ")
    mod1 = ensure_value("nct11af1_module", "Please input nct11af1 module type[tn]: ")

    print "=============="
    print "Report"
    print "  Serial number : %s" % serial
    print "  Operation mode : %s" % mode
    print "  Nct11af0 module type : %s" % mod0
    print "  Nct11af1 module type : %s" % mod1


if __name__ == "__main__":
    main()
