#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:13:27 2021

@author: n7
"""

import os
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def _install_dep(pkg_name):
    """
    Check is specified package is installed, and it not, install it via apt.

    Args:
        pkg_name (str): Name of the dependency to be checked.

    Returns:
        None.

    """
    if ("install ok installed" not in
            os.popen("dpkg -s " + pkg_name + " | grep Status").read()):
        os.system("sudo apt install " + pkg_name)
    else:
        print(pkg_name + " OK")


def _create_log_dir(logs_dir_path):
    """
    Create the specified directory to store logs, if not already present

    Args:
        logs_dir_path (str): Path of the directory to store logs.

    Returns:
        None.

    """
    os.system("mkdir -p \"" + logs_dir_path + "\"")


def _get_iw_devs():
    """
    Get the available wireless devices.

    Returns:
        devs_dict (dict): A dictionary consisting of the phy IDs as the keys
        and the interface names as the values.

    """
    dev_strs = os.popen("iw dev").read().split("phy#")[1:]
    devs_dict = {}
    for dev_str in dev_strs:
        phy_id = dev_str[:dev_str.find("\n")]
        if_name = dev_str.split("Interface ")[1]
        if_name = if_name[:if_name.find("\n")]
        devs_dict[phy_id] = if_name
    return devs_dict


def _get_iw_modes():
    """
    Get the supported modes of operation for each wireless device.

    Returns:
        modes_dict (dict): A dictionary consisting of the phy IDs as the keys
        and a list of available modes as the values.

    """
    list_strs = os.popen("iw list").read().split("Wiphy phy")[1:]
    modes_dict = {}
    for list_str in list_strs:
        phy_id = list_str[:list_str.find("\n")]
        modes_str = list_str.split("Supported interface modes:")[1].lstrip()
        modes_list = []
        for line in modes_str.split("\n"):
            if ("*" in line):
                modes_list.append(line.split("* ")[1])
            else:
                break
        modes_dict[phy_id] = modes_list
    return modes_dict


def _get_monitor_compatible_ifs():
    """
    Return a list of wireless interfaces that support monitor mode.

    Returns:
        monitor_if_names (list): Names of interfaces which support
        monitor mode.

    """
    devs = _get_iw_devs()
    modes = _get_iw_modes()
    monitor_if_names = []
    for dev in devs.items():
        if ("monitor" in modes[dev[0]]):
            monitor_if_names.append(dev[1])
    return monitor_if_names


def check(logs_dir_path=None):
    """

    Check if necessary dependencies are met, install missing packages and
    select an interface for sniffing.

    Args:
        logs_dir_path (str, optional): Path of the directory to store logs.
        If None, the default path (USER_HOME/pysniff_logs) is used.
        Defaults to None.

    Raises:
        RuntimeError: If no monitor-capable interface is found.

    Returns:
        str: Name of the interface selected for sniffing.
        logs_dir_path (str): Path of the logs directory.
        If a custom path is supplied to the function,
        the same path is returned.
        If not supplied, the default path is returned.

    """
    if logs_dir_path is None:
        logs_dir_path = os.path.join(os.path.expanduser("~"), "pysniff_logs")
    _install_dep("net-tools")
    _install_dep("wireless-tools")
    _install_dep("iw")
    monitor_if_names = _get_monitor_compatible_ifs()
    if (len(monitor_if_names) == 0):
        raise RuntimeError(
            "Wireless interface with monitor capability not found")
    else:
        print("Found interface(s) with monitor capbility. Selecting " +
              monitor_if_names[0])
    _install_dep("tshark")
    _create_log_dir(logs_dir_path)
    return (monitor_if_names[0], logs_dir_path)
