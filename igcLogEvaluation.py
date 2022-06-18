import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from readIGC import readLogFiles, readLogFilesList
import datetime
from colormap import createColormap
from threeDScatter import create3DScatter
import sys, os, getopt

# example: python igcLogEvaluation.py "../Paragleiten"

if __name__ == "__main__":
    num_arguments = len(sys.argv)
    if num_arguments < 2:
        raise Exception("Please provide a path or an igc logfile")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["filter", "delta_t=", "num_data_points="])
    except getopt.GetoptError:
        print("python igcLogEvaluation.py [options] <paths>")
        sys.exit(2)

    options = {}
    for opt, arg in opts:
        if opt == "--filter":
            options["filter"] = True
        elif opt == "--delta_t":
            delta_t = float(arg)
            options["delta_t"] = delta_t
        elif opt == "--num_data_points":
            num = int(arg)
            options["num_data_points"] = num

    if "delta_t" in options and "filter" not in options:
        print("delta_t gets ignored, because filtering is disabled.")

    if "num_data_points" in options and "filter" not in options:
        print("num_data_points gets ignored, because filtering is disabled")

    if "delta_t" in options and "num_data_points" in options:
        print("num_data_points gets ignored, because delta_t is used")


    log_files = []
    paths = []
    for path in args:
        (_, extension) = os.path.splitext(path)
        if extension and extension in [".IGC", ".igc"]:
            # valid igc file
            log_files.append(path)
        elif not extension:
            # folder
            paths.append(path)

    datasets = readLogFiles(paths, options)
    datasets.extend(readLogFilesList(log_files, options))

    if len(datasets) == 0:
        raise Exception("No logs found.")

    createColormap(datasets)
