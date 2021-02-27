#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:48:05 2021

@author: Nishad Mandlik
"""

from matplotlib import pyplot as plt
import pandas as pd

_COMMON_VENDORS = ["Samsung", "Motorola", "MediaTek", "Huawei", "Apple",
                   "Murata", "Intel", "OnePlus",  "Xiaomi"]

# LG, Sony, Panasonic, Google, RealMe


def _pie_labs(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)


def plot_mac_stats(dfs):
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
    vendor_counts.pop("Unknown", None)
    mac_stats_labs = ["Randomized", "Vendor Unknown", "Vendor Identified"]
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


# fig = plt.figure()  # create a figure object
# ax = fig.add_subplot(1, 1, 1)
# ax.hist(times_arr)
# ax.set_xlabel('Transport Time (ms)', fontsize='18')
# ax.set_ylabel('Frequency', fontsize='18')
# ax.set_title('Communication Latency For ' + protocol +
#              ' [' + label + 'Byte Data]', fontsize='20')
# # ax.legend(loc='lower right', fontsize=14)
# ax.tick_params(axis='both', which='major', labelsize=14)
# ax.tick_params(axis='both', which='minor', labelsize=10)
# plt.grid(True, which='both')
# plt.subplots_adjust(top=0.95,
#                     bottom=0.07,
#                     left=0.1,
#                     right=0.98,
#                     hspace=0.2,
#                     wspace=0.2)
