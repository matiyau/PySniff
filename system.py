#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:13:27 2021

@author: n7
"""

import os
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def _install_dep(pkg_name):
    if ("install ok installed" not in
            os.popen("dpkg -s " + pkg_name + " | grep Status").read()):
        os.system("sudo apt install " + pkg_name)
    else:
        print(pkg_name + " OK")


def _create_log_dir():
    os.system("mkdir -p \"" + os.path.join(_SCRIPT_DIR, "../logs") + "\"")


def _get_iw_devs():
    dev_strs = os.popen("iw dev").read().split("phy#")[1:]
    devs_dict = {}
    for dev_str in dev_strs:
        phy_id = dev_str[:dev_str.find("\n")]
        if_name = dev_str.split("Interface ")[1]
        if_name = if_name[:if_name.find("\n")]
        devs_dict[phy_id] = if_name
    return devs_dict


def _get_iw_modes():
    list_strs = os.popen("iw list").read().split("Wiphy phy")[1:]
    modes_dict = {}
    for list_str in list_strs:
        phy_id = list_str[:list_str.find("\n")]
        modes_str = list_str.split("Supported interface modes:")[1].lstrip()
        # print(modes_str)
        modes_list = []
        for line in modes_str.split("\n"):
            if ("*" in line):
                modes_list.append(line.split("* ")[1])
            else:
                break
        modes_dict[phy_id] = modes_list
    return modes_dict


def _get_monitor_compatible_ifs():
    devs = _get_iw_devs()
    modes = _get_iw_modes()
    monitor_if_names = []
    for dev in devs.items():
        if ("monitor" in modes[dev[0]]):
            monitor_if_names.append(dev[1])
    return monitor_if_names


def check():
    _install_dep("net-tools")
    _install_dep("wireless-tools")
    _install_dep("iw")
    monitor_if_names = _get_monitor_compatible_ifs()
    if (len(monitor_if_names) == 0):
        raise RuntimeError(
            "Wireless interface with monitor capability not found")
    else:
        print("Found interface(s) with monitor cpapbility. Selecting " +
              monitor_if_names[0])
    _install_dep("tshark")
    _create_log_dir()
    return monitor_if_names[0]
