#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:45:34 2021

@author: Nishad Mandlik
"""

import pysniff.utils as pu
import pysniff.plot as pp

PICKLE_DIR = "./logs/pickle"

dfs = pu.pickle_dir_to_dfs(PICKLE_DIR)
# dfs = {"Delft Station Cycle Stand":
#        pu.pickle_file_to_df("./logs/pickle/Delft Station Cycle Stand")}
# dfs = {"Residential Building Corridor":
#        pu.pickle_file_to_df("./logs/pickle/Residential Building Corridor")}
# dfs = {"Residential Building Mailbox Room":
#        pu.pickle_file_to_df("./logs/pickle/Residential Building Mailbox Room")}
# dfs = {"Residential Building Cycle Stand":
#        pu.pickle_file_to_df("./logs/pickle/Residential Building Cycle Stand")}

tot, rand, ven = pp.plot_mac_stats([df[1] for df in dfs.items()])

pp.plot_activity(dfs)

pp.plot_probe_detection_share(dfs)
