#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:19:25 2021

@author: n7
"""

import argparse
import os
import pysniff.system as system
from pysniff.interface import IF


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Capture and Log WiFi Packets")
    parser.add_argument("-t", default=0,
                        help="Time limit [in sec] for sniffing "
                        "(Default 0: infinite)")
    parser.add_argument("-l", default=None,
                        help="Directory path for storing log files "
                        "(Default none)")
    args = parser.parse_args()
    if_name, logs_dir = system.check(args.l)
    capt_if = IF(if_name, logs_dir)
    capt_if.capture(int(args.t))
