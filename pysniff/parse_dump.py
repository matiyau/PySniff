#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:05:42 2021

@author: Nishad Mandlik
"""

from datetime import datetime as dt
import dateutil.parser as dp
from mac_vendor_lookup import MacLookup
import math
import numpy as np
import os
import pandas as pd
import pyshark

_READ_FILT = "((wlan.fc.type_subtype==40 && !wlan.da==wlan.staa) || \
    (!wlan.fc.type_subtype==40 && !(wlan.fc.type_subtype==13 || \
                                    wlan.fc.type_subtype==24 || \
                                        wlan.fc.type_subtype==25)))"


class Dump():
    def __init__(self, file_paths, min_rssi=-70):
        """
        Generic interface for parsing multiple WireShark capture files.

        Args:
            file_paths (list): List of paths of WireShark capture files. Paths
                should be strings.
            min_rssi (int, optional): Minimum RSSI threshold (in dBm) for
                filtering packets. Packets with RSSI below this value will be
                discarded. Defaults to -70.

        Returns:
            None.

        """
        self.fps = file_paths
        self.set_min_rssi(min_rssi)
        self.reload()

    def set_min_rssi(self, rssi):
        """
        Set minimum RSSI for filtering. Updating this value should be followed
        by a call to 'reload', to update the filtered packets.

        Args:
            rssi (int): Minimum RSSI threshold (in dBm) for
                filtering packets. Packets with RSSI below this value will be
                discarded.

        Returns:
            None.

        """
        self.min_rssi = rssi

    def reload(self):
        """
        Reload the packets from the initially specified files.

        Returns:
            None.

        """
        self.rdfilt = _READ_FILT
        if (self.min_rssi != 0):
            self.rdfilt = self.rdfilt + " && wlan_radio.signal_dbm>=" + \
                str(self.min_rssi)
        self.packets = pd.DataFrame(columns=["Time", "MAC", "RSSI", "Channel",
                                             "Frame Type", "Frame Subtype"])
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
            print("")
            del capt
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

    def extract_devices(self):
        """
        Extract devices from the captured packets.

        Returns:
            pandas.DataFrame:
                Device parameters extracted from the captured packets.

        """
        devs = pd.DataFrame(columns=["MAC", "Vendor",
                                     "Times", "Frame Subtypes"])
        if (self.packets.empty):
            return devs
        macs = self.packets["MAC"].unique()
        ML = MacLookup()
        ML.update_vendors()
        for mac in macs:
            frames = self.packets.loc[self.packets["MAC"] == mac]
            if (mac[4] == "2" or mac[4] == "6" or mac[4] == "a" or
                    mac[4] == "e" or mac[4] == "A" or mac[4] == "E"):
                vendor = "Randomized"
            else:
                try:
                    vendor = ML.lookup(mac)
                except KeyError:
                    vendor = "Unknown"
            mins = np.unique(np.array([(60*tm.hour + tm.minute) for tm in
                                       frames["Time"]]))
            subtypes = frames["Frame Subtype"].unique()
            devs.loc[len(devs)] = [mac, vendor, mins, subtypes]
        return devs

    def __getitem__(self, frame_number):
        return self.packets.loc[frame_number]


class DumpFile(Dump):
    def __init__(self, file_path, min_rssi=-70):
        """
        Interface for parsing a single WireShark capture files.

       Args:
            file_path (str): Paths of WireShark capture files.
            min_rssi (int, optional): Minimum RSSI threshold (in dBm) for
                filtering packets. Packets with RSSI below this value will be
                discarded. Defaults to -70.

        Returns:
            None.

        """
        self.fp = file_path
        Dump.__init__(self, [self.fp], min_rssi)


class DumpDir(Dump):
    def __init__(self, dir_path, min_rssi=-70):
        """
        Interface for parsing WireShark capture files from the same directory.

       Args:
            dir_path (str): Paths of WireShark capture directory.
            min_rssi (int, optional): Minimum RSSI threshold (in dBm) for
                filtering packets. Packets with RSSI below this value will be
                discarded. Defaults to -70.

        Returns:
            None.

        """
        self.dp = dir_path
        Dump.__init__(self, self._get_file_paths(), min_rssi)

    def _get_file_paths(self):
        """
        Get a list of paths of all files present in the initially specified
        capture directory.

        Returns:
            list: List of paths of all files from the capture directory.

        """
        item_paths = [os.path.join(self.dp, item_name) for item_name in
                      os.listdir(self.dp)]
        return [fp for fp in item_paths if os.path.isfile(fp)]

    def reload(self):
        """
        Reload packets from all files in the intially specified directory.

        Returns:
            None.

        """
        self.fps = self._get_file_paths()
        Dump.reload(self)
