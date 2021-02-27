#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:10:30 2021

@author: Nishad Mandlik
"""

from pysniff.parse_dump import DumpFile, DumpDir
import nest_asyncio

nest_asyncio.apply()

g = DumpFile("../logs/Delft Station/wlx00c0ca98ef18_20210217_180452")
# g = DumpDir("../logs/VHL Mailbox")
k = g.extract_devices()

k.to_pickle("temp_comp", compression="gzip")
