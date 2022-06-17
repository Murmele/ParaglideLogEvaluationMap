from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

# install Tkinter: sudo pacman -S tk
# https://stackoverflow.com/questions/48504746/importerror-libtk8-6-so-cannot-open-shared-object-file-no-such-file-or-direct

def create3DScatter(datasets, latlim=(46.59460, 46.63691), longlim=(11.10284,11.18239)): # default near around vigiljoch

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    data = np.random.rand(3, 100)
    x, y, z = data  # for show
    c = np.arange(len(x)) / len(x)  # create some colours

    use_gps_climb_rate = True

    climb_rate_min = -4
    climb_rate_max = 3

    # if use_gps_climb_rate:
    #     colors = dataset['climb_rate_gps']
    # else:
    #     colors = dataset['climb_rate_baro']

    for dataset in datasets:
        if len(dataset["time"]) == 0:
            continue
        try:
            if dataset["lat"].min() < latlim[0] or dataset["lat"].max() > latlim[1] or dataset["long"].min() < longlim[0] or dataset["long"].max() > longlim[1]:
                continue
        except ValueError:
            continue
        color = dataset['climb_rate_gps']
        p = ax.scatter(dataset['lat'], dataset['long'], dataset['alt_gps'], c=color, cmap=plt.get_cmap("jet"), vmin=climb_rate_min, vmax=climb_rate_max)
    # ax.set_xlabel('$\psi_1$')
    # ax.set_ylabel('$\Phi$')
    # ax.set_zlabel('$\psi_2$')
    if p:
        ax.set_box_aspect([np.ptp(i) for i in data])  # equal aspect ratio

        fig.colorbar(p, ax=ax)

        plt.show()

    #
    #
    # for dataset in datasets:
    #     if use_gps_climb_rate:
    #         colors = dataset['climb_rate_gps']
    #     else:
    #         colors = dataset['climb_rate_baro']
    #
    #     if not len(colors):
    #         continue
    #     try:
    #         color_line = features.ColorLine(
    #             positions=list(zip(dataset['lat'], dataset['long'])),
    #             colors=colors,
    #             colormap=colormap,
    #             weight=10)
    #     except ValueError as e:
    #         print(e)
    #
    #     color_line.add_to(m)