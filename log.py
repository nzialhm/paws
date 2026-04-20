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
            if not os.path.exists(LOG_DIR):
                os.makedirs(LOG_DIR)

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_path = os.path.join(LOG_DIR, LOG_FILE)

            with open(log_path, "a") as f:
                if isinstance(msg, unicode):
                    msg = msg.encode('utf-8')
                f.write("[{}] {}\n".format(timestamp, msg))

        except Exception as e:
            print("LOG ERROR:", str(e))
