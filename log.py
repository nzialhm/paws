#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

LOG_DIR = "/nct11af/pawslog"
LOG_FILE = "paws.log"

def write_log(msg):
    if sys.platform.startswith('win'):
        print(msg)
    else:
        try:
            # 1. 디렉토리 없으면 생성
            if not os.path.exists(LOG_DIR):
                os.makedirs(LOG_DIR)

            # 2. 시간 추가
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            log_path = os.path.join(LOG_DIR, LOG_FILE)

            # 3. 파일 append
            with open(log_path, "a") as f:
                f.write("[{}] {}\n".format(timestamp, msg))

        except Exception as e:
            # 로그 실패 시 콘솔 fallback
            print("LOG ERROR:", e)
