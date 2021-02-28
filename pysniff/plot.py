#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:48:05 2021

@author: Nishad Mandlik
"""

from matplotlib import pyplot as plt
import numpy as np
import operator
import pandas as pd

_COMMON_VENDORS = ["Apple", "Huawei", "Google", "Intel", "MediaTek", "LG", "Motorola", "Murata",
                   "OnePlus", "Panasonic", "Samsung", "Sony", "Xiaomi"]


def plot_mac_stats(dfs):
    """
    Plot pie-charts of randomization percentages and vendor share among all
    MAC addresses from all supplied dataframes.

    Args:
        dfs (list): Dataframes of device details.

    Returns:
        tuple:
            Contains the following stats:
            devices_count (int): Total number of detected devices.
            rand_count (int): Number of devices with randomized MAC addresses.
            vendor_counts (dict): Number of devices of each vendor.

    """
    if (type(dfs) is pd.DataFrame):
        dfs = [dfs]
    devices_count = 0
    rand_count = 0
    vendor_counts = {vendor: 0 for vendor in _COMMON_VENDORS}
    vendor_counts["Unknown"] = 0
    vendor_counts["Other"] = 0
    for df in dfs:
        devices_count = devices_count + len(df)
        df_tmp = df[df["Vendor"] != "Randomized"]
        non_rand_cnt = len(df_tmp)
        rand_count = rand_count + (len(df) - non_rand_cnt)
        df_filt = df_tmp[df_tmp["Vendor"] != "Unknown"]
        vendor_counts["Unknown"] += (non_rand_cnt - len(df_filt))
        detected_vendors = df_filt["Vendor"].str.lower()
        for com_ven in _COMMON_VENDORS:
            for index in detected_vendors.index:
                if com_ven.lower() in detected_vendors[index]:
                    vendor_counts[com_ven] = vendor_counts[com_ven]+1
                    detected_vendors.drop(index, inplace=True)
        vendor_counts["Other"] += len(detected_vendors)

    fig = plt.figure()  # create a figure object
    ax = fig.add_subplot(1, 1, 1)
    mac_stats_labs = ["Randomized", "Vendor Unknown", "Vendor Identified"]
    wedges, texts, autotexts = ax.pie([rand_count,
                                       (devices_count-rand_count -
                                        vendor_counts["Unknown"]),
                                       vendor_counts["Unknown"]],
                                      labels=mac_stats_labs,
                                      startangle=90,
                                      colors=["tab:green", "tab:red",
                                              "tab:orange"],
                                      autopct="%1.1f%%",
                                      pctdistance=0.7,
                                      labeldistance=1.05)
    ax.set_title("MAC Address Vendor Lookup", fontweight="bold")
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=10, weight="bold")
    plt.show()

    fig = plt.figure()  # create a figure object
    ax = fig.add_subplot(1, 1, 1)
    unknown_count = vendor_counts.pop("Unknown", 0)
    other_count = vendor_counts.pop("Other", 0)
    vendor_counts = dict(sorted(vendor_counts.items(),
                                key=operator.itemgetter(1), reverse=True))
    vendor_counts_tmp = {}
    for (k, v) in vendor_counts.items():
        if (v/(devices_count-rand_count-unknown_count) > 0.03):
            vendor_counts_tmp[k] = v
        else:
            other_count += v
    vendor_counts = vendor_counts_tmp
    vendor_counts["Other"] = other_count
    wedges, texts, autotexts = ax.pie(list(vendor_counts.values()),
                                      labels=list(vendor_counts.keys()),
                                      startangle=90,
                                      autopct="%1.1f%%",
                                      pctdistance=0.8,
                                      labeldistance=1.05)
    ax.set_title("Identified MAC Address Vendors", fontweight="bold")
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=10, weight="bold")
    plt.show()

    return (devices_count, rand_count, vendor_counts)


def plot_activity(dfs):
    """
    Plot crowd activity stats for each dataframe present in the dictionary.
    Activity is shown as a histogram of number of devices present at the
    location in a particular 30 minute interval.

    Args:
        dfs (dict): Dataframes of device details.
            Dictionary keys are strings specifying the file name. Their
            corresponding values are of type 'pandas.DataFrame'.

    Returns:
        None.

    """
    maj_interval = 180
    min_interval = 30
    for (loc, df) in dfs.items():
        sample_times = np.array([])
        for times in df["Times"]:
            sample_times = np.concatenate([sample_times,
                                           np.unique(times -
                                                     times % min_interval)])
        fig = plt.figure()  # create a figure object
        ax = fig.add_subplot(1, 1, 1)
        # ax.plot(range(1, len(counts) + 1), counts)
        ax.hist(sample_times, bins=np.arange(0, 1441, min_interval))
        ax.set_xlabel('Time [hh:mm]', fontsize='18')
        ax.set_ylabel('No. of Devices', fontsize='18')
        ax.set_title('Device Activity at \n' + loc, fontsize='20')
        # ax.legend(loc='lower right', fontsize=14)
        ax.set_xlim(0, 1440)
        ax.set_xticks([i for i in range(0, 1440, min_interval)
                       if i % maj_interval], minor=True)
        ax.set_xticks(np.arange(0, 1440, maj_interval))
        ax.set_xticklabels(labels=["%02d:00" % i for i in range(0, 24, 3)],
                           rotation=90)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        plt.grid(True, which='both')
        plt.subplots_adjust(top=0.93,
                            bottom=0.2,
                            left=0.11,
                            right=0.98,
                            hspace=0.2,
                            wspace=0.2)


def plot_probe_detection_share(dfs):
    """
    Plot pie-chart of percentage of devices detected without any probe request
    and that of devices detected with at least one probe request

    Args:
        dfs (dict): Dataframes of device details.
            Dictionary keys are strings specifying the file name. Their
            corresponding values are of type 'pandas.DataFrame'.

    Returns:
        None.

    """
    for (loc, df) in dfs.items():
        total_devs = len(df)
        non_probes = 0
        for i in df["Frame Subtypes"]:
            if 4 not in i:
                non_probes += 1
        fig = plt.figure()  # create a figure object
        ax = fig.add_subplot(1, 1, 1)
        packet_labs = ["Probe Request", "Other"]
        wedges, texts, autotexts = ax.pie([total_devs - non_probes,
                                           non_probes],
                                          labels=packet_labs,
                                          startangle=90,
                                          colors=["tab:green", "tab:red"],
                                          autopct="%1.1f%%",
                                          pctdistance=0.82,
                                          labeldistance=1.05)
        ax.set_title("Means of Device Detection at\n" + loc, fontweight="bold")
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=10, weight="bold")
        plt.show()
