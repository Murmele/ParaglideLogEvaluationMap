# https://github.com/fhorinek/SkyDrop/tree/master/skydrop# read in data
from aerofiles.igc import Reader
import numpy as np
import datetime
import os
import scipy.ndimage

def readLogFilesList(files_relpath):
    """
    Read provided logfiles
    :param files_relpath:
    :return:
    """
    datasets = list()
    for rel_path in files_relpath:
        abs_path = os.path.abspath(rel_path)
        d = parse_data_set(abs_path)
        if d is not None:
            datasets.append(d)
    return datasets

def readLogFiles(rel_paths_logs):
    """
    Find all .IGC/.igc files in a list of relative paths
    :param rel_paths_logs: list of relative paths
    :return:
    """
    logs = list()
    for rel_path in rel_paths_logs:
        for subdir, dirs, files in os.walk(rel_path):
            for file in files:
                (root, extension) = os.path.splitext(file)
                if extension in [".IGC", ".igc"]:
                    logs.append(os.path.join(subdir, file))

    print(logs)

    return readLogFilesList(logs)


def datetime_time_to_seconds(time):
    return time.hour * 3600 + time.minute * 60 + time.second + time.microsecond / 1000


def parse_data_set(abs_path):
    with open(abs_path, 'r') as f:
        try:
            parsed_igc_file = Reader().read(f)
        except UnicodeDecodeError as e:
            print(abs_path)
            return None

    dataset = dict()
    use_interpoltated_data = True

    records = parsed_igc_file['fix_records'][1]
    nb_elements = len(records)

    time = np.arange(nb_elements, dtype=datetime.time)
    if len(time) == 0:
        print(f"File {abs_path} does not contain any data")
        return None
    time_seconds = np.arange(nb_elements, dtype=float)
    long = np.arange(nb_elements, dtype=float)
    lat = np.arange(nb_elements, dtype=float)
    alt_baro = np.arange(nb_elements, dtype=float)
    alt_gps = np.arange(nb_elements, dtype=float)

    for i in range(len(records)):
        record = records[i]
        time[i] = record['time']
        time_seconds[i] = datetime_time_to_seconds(time[i])
        long[i] = record['lon']
        lat[i] = record['lat']
        alt_baro[i] = record['pressure_alt']
        alt_gps[i] = record['gps_alt']

    if use_interpoltated_data:
        time_seconds_new = np.linspace(int(min(time_seconds)), int(max(time_seconds)), num=1000)
        alt_gps_new = np.interp(time_seconds_new, time_seconds, alt_gps)
        alt_baro_new = np.interp(time_seconds_new, time_seconds, alt_baro)

        # ayvri uses a gaussian convolution filter with variance 10, and samples = 10
        # https://stackoverflow.com/questions/25216382/gaussian-filter-in-scipy
        # w number of samples used in the filter to filter for the next (5 left side, 5 rightside)
        # w = 2*(int(truncate*sigma + 0.5)
        # factor =  5 <= truncate*sigma + 0.5 < 6
        factor = 5
        truncate = 4
        sigma = (factor - 0.5)/truncate
        alt_gps = scipy.ndimage.gaussian_filter1d(alt_gps_new, sigma=sigma, order=0, truncate=truncate)
        alt_baro = scipy.ndimage.gaussian_filter1d(alt_baro_new, sigma=sigma, order=0, truncate=truncate)
        lat = np.interp(time_seconds_new, time_seconds, lat)
        long = np.interp(time_seconds_new, time_seconds, long)

        time_seconds = time_seconds_new


    # differentiate
    diff_alt_baro = np.diff(alt_baro)
    diff_alt_gps = np.diff(alt_gps)
    time_diff = np.diff(time_seconds)

    # %% calculate distance between two data points
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

    R = 6373.0  # radius earth [km]

    dlon = np.radians(np.diff(long))
    dlat = np.radians(np.diff(lat))

    distance = np.arange(len(long) - 1, dtype=float)
    distance_total = np.arange(len(long) - 1, dtype=float)

    for i in range(len(long) - 1):
        a = (np.sin(dlat[i] / 2)) ** 2 + np.cos(np.radians(lat[i])) * np.cos(np.radians(lat[i + 1])) * (
            np.sin(dlon[i] / 2)) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance[i] = R * c  # [km]
        distance_total[i] = distance_total[i - 1] + distance[i] if i > 0 else distance[i]  # [km]

    dataset['time'] = time[:-1]
    dataset['time_seconds'] = time_seconds[:-1]
    dataset['long'] = long[:-1]
    dataset['lat'] = lat[:-1]
    dataset['alt_baro'] = alt_baro[:-1]
    dataset['alt_gps'] = alt_gps[:-1]
    dataset['distance'] = distance  # [km]
    dataset['distance_total'] = distance_total
    dataset['data_path'] = abs_path
    dataset['glide_ratio'] = distance * 1000 / diff_alt_gps

    dataset['climb_rate_baro'] = diff_alt_baro / time_diff
    dataset['climb_rate_gps'] = diff_alt_gps / time_diff

    return dataset