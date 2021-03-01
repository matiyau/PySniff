#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:10:30 2021

@author: Nishad Mandlik
"""

import pysniff.utils as pu
import nest_asyncio

nest_asyncio.apply()
pu.pcap_dir_to_pickle("./logs/pcap_filt", out_dir_path="./logs/pickle")

# pu.pcap_dir_to_pickle(
#     "./logs/pcap/Delft Station Cycle Stand (Weekend)", out_dir_path="./logs/pickle")
