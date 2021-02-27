#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:45:34 2021

@author: Nishad Mandlik
"""

import pysniff.utils as pu
import pysniff.plot as pp

dfs = pu.pickle_dir_to_dfs("./logs/pickle")

tot, rand, ven = pp.plot_mac_stats([df[1] for df in dfs.items()])

pp.plot_activity(dfs)

# pp.plot_probe_detection_share(dfs)
