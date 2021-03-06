#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 18:42:40 2021

@author: Nishad Mandlik
"""

from datetime import datetime
import getmac
import os
from pysniff import system


class IF():
    def __init__(self, if_name, log_dir_path):
        """
        Class for the interface which is to be used for sniffing.

        Args:
            if_name (str): Name of the wireless interface.
            log_dir_path (str): Path of the directory to store logs.

        Returns:
            None.

        """
        self.if_name = if_name
        self.log_dir = log_dir_path

    def _cfg(self, mode):
        """
        Configure the interface to operate in the specified mode.

        Args:
            mode (str): Wireless interface mode.

        Returns:
            None.

        """
        os.system("sudo systemctl stop network-manager")
        os.system("sudo ifconfig " + self.if_name + " down")
        os.system("sudo iwconfig " + self.if_name + " mode " + mode)
        os.system("sudo ifconfig " + self.if_name + " up")
        os.system("sudo systemctl start network-manager")

    def _cfg_monitor(self):
        """
        Configure the interface to operate in monitor mode.

        Returns:
            None.

        """
        self._cfg("monitor")

    def _cfg_managed(self):
        """
        Configure the interface to operate in managed mode.

        Returns:
            None.

        """
        self._cfg("managed")

    def _generate_log_path(self):
        """
        Generate the path for the log file, based on the current timestamp.

        Returns:
            str:
                Path of the log file.

        """
        file_name = self.if_name + "_" + \
            datetime.today().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.log_dir, file_name)

    def capture(self, time_sec=0):
        """
        Capturing and log packets.

        Args:
            time_sec (int, optional): Number of seconds for which sniffing
                should to be done. 0 to run indefinitely. Defaults to 0.

        Returns:
            None.

        """
        self._cfg_monitor()
        log_path = self._generate_log_path()

        ifs_filt = "not ("
        for iface in system.get_iw_devs().items():
            if_mac = getmac.get_mac_address(interface=iface[1])
            ifs_filt = ifs_filt + "wlan ra " + if_mac + " or \
                wlan ta " + if_mac + " or "
        ifs_filt = ifs_filt[:-4] + ")"

        '''
        !(wlan.fc.type_subtype==1 || wlan.fc.type_subtype==3 ||
          wlan.fc.type_subtype==5 || wlan.fc.type_subtype==8 ||
          wlan.fc.type_subtype==11 || wlan.fc.type_subtype==12 ||
          wlan.fc.type_subtype==27 || wlan.fc.type_subtype==28 ||
          wlan.fc.type_subtype==29 || wlan.fc.type_subtype==32)
        '''
        filt = " -f \"not (subtype assoc-resp or \
            subtype reassoc-resp or subtype probe-resp or subtype beacon or \
            subtype auth or subtype deauth or subtype rts or subtype cts or \
            subtype ack or subtype cf-end or subtype cf-end-ack or \
            subtype data) && " + ifs_filt + "\""
        if (time_sec == 0):
            # Works with timeout 0 also, but Ctrl+C capability is lost when
            # timeout is used.
            os.system("dumpcap -I -i " + self.if_name + " -w \"" +
                      log_path + "\"" + filt)
        elif (time_sec > 0):
            os.system("timeout " + str(time_sec) + " dumpcap -I -i " +
                      self.if_name + " -w \"" + log_path + "\"" + filt)
        self._cfg_managed()

        '''
        Add these extra filters during display. (not available in pcap syntax)

        ((wlan.fc.type_subtype==40 && !wlan.da==wlan.staa) ||
         (!wlan.fc.type_subtype==40 && !(wlan.fc.type_subtype==13 ||
                                         wlan.fc.type_subtype==24 ||
                                         wlan.fc.type_subtype==25)))
        '''
