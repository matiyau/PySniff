#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:05:42 2021

@author: Nishad Mandlik
"""

from datetime import datetime as dt
import dateutil.parser as dp
import math
import os
import pandas as pd
import pyshark

_READ_FILT = "((wlan.fc.type_subtype==40 && !wlan.da==wlan.staa) || \
    (!wlan.fc.type_subtype==40 && !(wlan.fc.type_subtype==13 || \
                                    wlan.fc.type_subtype==24 || \
                                        wlan.fc.type_subtype==25)))"


class Dump():
    def __init__(self, file_paths, min_rssi=None):
        self.fps = file_paths
        self.rdfilt = _READ_FILT
        if (min_rssi != 0):
            if (min_rssi is None):
                min_rssi = -70
            self.rdfilt = self.rdfilt + " && wlan_radio.signal_dbm>=" + \
                str(min_rssi)
        self.reload()

    def reload(self):
        self.packets = pd.DataFrame(columns=["time", "mac", "rssi", "channel",
                                             "frame_type", "frame_subtype"])
        i = 1

        for fp in self.fps:
            tmp_file = ".tmp_" + str(math.floor(dt.now().timestamp()))
            os.system("tshark -2 -R '" + self.rdfilt + "' -r '" + fp +
                      "' -w '" + tmp_file + "'")
            capt = pyshark.FileCapture(input_file=tmp_file, keep_packets=False)
            while True:
                try:
                    pkt = capt.next()
                except StopIteration:
                    break
                attr = dir(pkt.wlan)
                if ("ta" in attr):
                    addr = pkt.wlan.ta
                elif ("sa" in attr):
                    addr = pkt.wlan.sa
                elif ("bssid" in attr):
                    addr = pkt.wlan.bssid
                else:
                    continue

                if ("signal_dbm" in dir(pkt.wlan_radio)):
                    rssi = int(pkt.wlan_radio.signal_dbm)
                else:
                    continue
                frame_control = int(pkt.wlan.fc, 0) >> 8
                self.packets.loc[i] = [dp.parse(pkt.frame_info.time), addr,
                                       rssi, int(pkt.wlan_radio.channel),
                                       (frame_control & 0b00001100) >> 2,
                                       (frame_control & 0b11110000) >> 4]
                print(str(i), end='\r', flush=True)
                i = i+1
            del capt
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

    def set_disp_filt(self, disp_filt):
        self.disp_filt = disp_filt


class DumpFile(Dump):
    def __init__(self, file_path, min_rssi=None):
        self.fp = file_path
        Dump.__init__(self, [self.fp], min_rssi)


class DumpDir(Dump):
    def __init__(self, dir_path, min_rssi=None):
        self.dp = dir_path
        Dump.__init__(self, self._get_file_paths(), min_rssi)

    def _get_file_paths(self):
        item_paths = [os.path.join(self.dp, item_name) for item_name in
                      os.listdir(self.dp)]
        return [fp for fp in item_paths if os.path.isfile(fp)]

    def reload(self):
        self.fps = self._get_file_paths()
        Dump.reload(self)
