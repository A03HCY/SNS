#-*- coding:utf-8 -*-

import threading as td
import socket    as line
import time

__verson__ = '0.3.1'

def HostIP():
    try:
        s = line.socket(line.AF_INET, line.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip