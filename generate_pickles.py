#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:10:30 2021

@author: Nishad Mandlik
"""

import pysniff.utils as pu
import nest_asyncio

IN_DIR = "./logs/pcap_filt"
OUT_DIR = "./logs/pickle"

nest_asyncio.apply()

pu.pcap_dir_to_pickle(IN_DIR, out_dir_path=OUT_DIR)

# pu.pcap_dir_to_pickle(
#     "./logs/pcap/Delft Station Cycle Stand (Weekend)", out_dir_path="./logs/pickle")
