import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm
from mpl_toolkits import basemap

import math
import numpy as np
from scipy import interpolate

from build_data import build_city_data, build_plot_data
from plot_data import plot_chart

cities = build_city_data()

names, pop_fns, lats, longs, colors = build_plot_data(cities)

# Plot parameters
t = 2011
pop_limit = 100000
num_top_cities = 50
save_img = False

# Plots
fig = plt.figure(figsize=(9,10.8), tight_layout=True)

plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors,
           compress_pops = False, save_img = save_img, in_animation = False, show_map = True, show_map_labels = True, show_chart = False)

