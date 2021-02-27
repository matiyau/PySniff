#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 04:03:11 2021

@author: Nishad Mandlik
"""

import os
import pandas as pd
from pysniff.parse_dump import DumpFile, DumpDir


def pcap_file_to_pickle(in_file_path, out_file_path=None, out_dir_path=None):
    """
    Extract the devices from a pcap dump files in a directory and write the
    resultant dataframe to a pickle file.

    Args:
        in_dir_path (str): Path of the input pcap file.
        out_file_path (str, optional): Path of the output pickle file.
            Defaults to None.
        out_dir_path (str, optional): Path of the directory in which the
            output pickle file should be stored. Defaults to None.

    Raises:
        TypeError: Raised when both or none among 'out_file_path' and
            'out_dir_path' is of NoneType.

    Returns:
        None.

    """
    if out_file_path is None and out_dir_path is None:
        raise TypeError("Both 'out_file_path' and 'out_dir_path' cannot be \
                        NoneType variables")
    if out_file_path is not None and out_dir_path is not None:
        raise TypeError("Only one of 'out_file_path' and 'out_dir_path' \
                        should be a NoneType variable")
    if out_file_path is None:
        out_file_path = os.path.join(out_dir_path,
                                     os.path.split(in_file_path)[1])
    print("File: " + os.path.split(in_file_path)[1])
    os.system("mkdir -p '" + os.path.split(out_file_path)[0] + "'")
    print("Reading pcap...")
    DF = DumpFile(in_file_path)
    print("Extracting Devices...")
    devs = DF.extract_devices()
    print("Writing Pickle...")
    devs.to_pickle(out_file_path, compression="gzip")
    print("Done\n")


def pcap_dir_to_pickle(in_dir_path, out_file_path=None, out_dir_path=None,
                       recursive=True):
    """
    Extract the devices from a pcap dump files in a directory and write the
    resultant dataframe to a pickle file.

    Args:
        in_dir_path (str): Path of the directory which contains the pcap files.
        out_file_path (str, optional): Path of the output pickle file.
            Defaults to None.
        out_dir_path (str, optional): Path of the directory in which the
            output pickle file should be stored. Defaults to None.
        recursive (boolean, optional): Whether the input directory should be
            read recursively or not. Defaults to True.

    Raises:
        TypeError: Raised when both or none among 'out_file_path' and
            'out_dir_path' is of NoneType. Additionally, in recursive mode,
            it is raised when 'out_dir_path' is not provided.

    Note:
        Exactly one among 'out_file_path' and 'out_dir_path' should be
        specified. In recursive mode, it is mandatory to specify
        'out_dir_path'. Thus, in this mode, 'out_file_path' must be None.

    Returns:
        None.

    """
    if out_file_path is None and out_dir_path is None:
        raise TypeError("Both 'out_file_path' and 'out_dir_path' cannot be \
                        NoneType variables.")
    if out_file_path is not None and out_dir_path is not None:
        raise TypeError("Only one of 'out_file_path' and 'out_dir_path' \
                        should be a NoneType variable.")
    if (recursive):
        if (out_file_path is not None):
            raise TypeError("In recursive mode, 'out_file_path' must be None,\
                            and 'out_dir_path' must be specified.")
        in_dir_paths = [root for (root, _, _) in os.walk(in_dir_path)]
    else:
        in_dir_paths = [in_dir_path]
    for path in in_dir_paths:
        if out_file_path is None:
            out_file_path = os.path.join(out_dir_path,
                                         os.path.split(path)[1])
        print("Directory: " + os.path.split(path)[1])
        os.system("mkdir -p '" + os.path.split(out_file_path)[0] + "'")
        print("Reading pcap(s)...")
        DD = DumpDir(path)
        print("Extracting Devices ...")
        devs = DD.extract_devices()
        if not devs.empty:
            print("Writing Pickle...")
            devs.to_pickle(out_file_path, compression="gzip")
        else:
            print("Nothing to write")
        print("Done\n")
        out_file_path = None


def pickle_file_to_df(pickle_file_path):
    """
    Read a dataframe from a pickle file.

    Args:
        pickle_file_path (str): Path of the input pickle file.

    Returns:
        pandas.DataFrame:
            Dataframe of device details.

    """
    return pd.read_pickle(pickle_file_path, compression="gzip")


def pickle_dir_to_dfs(pickle_dir_path):
    """
    Read a dataframes from all pickle files in a directory.

    Args:
        pickle_dir_path (str): Path of the directory containing the pickle
        files.

    Returns:
        dict:
            Dataframes of device details from all pickle files.
            Dictionary keys are strings specifying the file name. Their
            corresponding values are of type 'pandas.DataFrame'

    """
    dfs = {}
    for item in os.listdir(pickle_dir_path):
        pickle_file_path = os.path.join(pickle_dir_path, item)
        if not os.path.isfile(pickle_file_path):
            continue
        df = pd.read_pickle(pickle_file_path, compression="gzip")
        if (df.empty):
            continue
        dfs[item] = df
    return dfs
