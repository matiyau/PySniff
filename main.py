#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:19:25 2021

@author: n7
"""

import system
from capture import IF


if __name__ == '__main__':
    if_name = system.check()
    interface = IF(if_name)
    interface.start()
