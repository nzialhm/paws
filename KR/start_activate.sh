#!/bin/sh

# 1. 인터페이스 생성 대기
while ! ls /proc/nct11af/ 2>/dev/null | grep -q "nct11af1"; do
    sleep 2
done

echo "nct11af1 exist"

# 2. 인터페이스 활성 대기
while ! ifconfig nct11af1 >/dev/null 2>&1; do
    sleep 2
done

echo "nct11af1 active"

# 3. 즉시 실행 (백그라운드)
(
    /nct11af/script/tvwsDB/check_activate.py > /dev/null 2>&1
) &
