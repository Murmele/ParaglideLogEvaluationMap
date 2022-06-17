import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from readIGC import readLogFiles, readLogFilesList
import datetime
from colormap import createColormap
from threeDScatter import create3DScatter
import os
import sys

# example: python igcLogEvaluation.py "../Paragleiten"

if __name__ == "__main__":
    num_arguments = len(sys.argv)
    if num_arguments < 2:
        raise Exception("Please provide a path or an igc logfile")


    log_files = []
    paths = []
    for i in range(1, num_arguments):
        argument = sys.argv[i]
        (_, extension) = os.path.splitext(argument)
        if extension and extension in [".IGC", ".igc"]:
            # valid igc file
            log_files.append(argument)
        elif not extension:
            # folder
            paths.append(argument)

    datasets = readLogFiles(paths)
    datasets.extend(readLogFilesList(log_files))

    if len(datasets) == 0:
        raise Exception("No logs found.")

    createColormap(datasets)
