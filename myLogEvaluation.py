import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from readIGC import readLogFiles, readLogFilesList
import datetime
from colormap import createColormap
from threeDScatter import create3DScatter
import os
import sys


if __name__ == "__main__":
    rel_path_logs = '../Paragleiten'

    log_files = [os.path.join(rel_path_logs, "Martin/LOGS/2022/06-14/01-1712.IGC"),
                 os.path.join(rel_path_logs, "Sophie/LOGS/2022/06-14/01-1705.IGC"),
            ]

    #datasets = readLogFiles([rel_path_logs])
    datasets = readLogFilesList(log_files)

    # plt.figure(figsize=(20, 10))
    #
    # counter = 0
    # for dataset in datasets:
    #     plot = plt.plot(dataset['distance_total'], dataset['alt_baro'], label=logs[counter]+"_baro")
    #     plot = plt.plot(dataset['distance_total'], dataset['alt_gps'], label=logs[counter]+"_gps")
    #     counter += 1
    #plt.legend()

    createColormap(datasets)
    #create3DScatter(datasets)
