#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 18:42:40 2021

@author: n7
"""

import os
from datetime import datetime


_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class IF():
    def __init__(self, if_name):
        """
        Class for the interface which is ot be used for sniffing.

        Args:
            if_name (str): Name of the wireless interface.

        Returns:
            None.

        """
        self.if_name = if_name

    def _cfg(self):
        """
        Configure the interface to operate in monitor mode.

        Returns:
            None.

        """
        os.system("sudo ifconfig " + self.if_name + " down")
        os.system("sudo iwconfig " + self.if_name + " mode monitor")
        os.system("sudo ifconfig " + self.if_name + " up")

    def _generate_log_path(self):
        """
        Generate the path for the log file, based on the current timestamp.

        Returns:
            str: Path of the log file.

        """
        file_name = self.if_name + "_" + \
            datetime.today().strftime("%Y%m%d_%H%M%S")
        return os.path.join(_SCRIPT_DIR, "../logs/" + file_name)

    def start(self):
        """
        Start sniffing.

        Returns:
            None.

        """
        self._cfg()
        log_path = self._generate_log_path()
        os.system("tshark -I -i " + self.if_name + " -w \"" + log_path + "\"")
