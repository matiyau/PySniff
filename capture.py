#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:19:25 2021

@author: n7
"""

import pysniff.system as system
from pysniff.interface import IF


if __name__ == '__main__':
    if_name, logs_dir = system.check()
    capt_if = IF(if_name, logs_dir)
    capt_if.capture()
