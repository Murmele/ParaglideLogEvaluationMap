import os
import folium
from folium import features
from branca.colormap import LinearColormap
import webbrowser
# https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/Features.ipynb#ColorLine
# https://python-visualization.github.io/folium/modules.html#folium.features.ColorLine

def createColormap(datasets, location=[46.6116, 11.1630]): # default lana
    m = folium.Map(location=location, zoom_start=12)

    # legend
    vmin = -5 #np.min(colors)
    vmax = 5 #np.max(colors)
    colormap = LinearColormap(['b', 'g', 'y', 'r', 'm'], vmin=vmin, vmax=vmax)
    colormap.caption = "Climb rate"
    colormap.add_to(m)

    use_gps_climb_rate = False

    for dataset in datasets:
        if use_gps_climb_rate:
            colors = dataset['climb_rate_gps']
        else:
            colors = dataset['climb_rate_baro']

        if not len(colors):
            continue
        try:
            color_line = features.ColorLine(
                positions=list(zip(dataset['lat'], dataset['long'])),
                colors=colors,
                colormap=colormap,
                nb_steps=100,
                weight=10)
        except ValueError as e:
            print(e)

        color_line.add_to(m)

    if not os.path.isdir('results'):
        os.makedirs('results')
    f = os.path.join('results', 'Features_0.html')
    m.save(f)
    webbrowser.open(f)
