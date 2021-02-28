#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:10:30 2021

@author: Nishad Mandlik
"""

import pysniff.utils as pu
import nest_asyncio

nest_asyncio.apply()
# pu.pcap_dir_to_pickle("./logs/pcap", out_dir_path="./logs/pickle")

pu.pcap_dir_to_pickle(
    "./logs/pcap/Residential Building Corridor", out_dir_path="./logs/pickle")
