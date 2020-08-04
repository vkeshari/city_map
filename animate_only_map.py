import matplotlib.pyplot as plt
from matplotlib import animation

import numpy as np

from build_data import build_city_data, build_plot_data
from plot_data import plot_chart

cities = build_city_data()

names, pop_fns, lats, longs, colors = build_plot_data(cities)

start_year = 1901
end_year = 2012
speed_multiplier = 3

num_top_cities = 50
interval = (0.06 - 0.001 * num_top_cities) * speed_multiplier
file_name = 'output/animated_only_map_no_labels_' + str(num_top_cities) + '_' + str(start_year) + '_' + str(end_year) + '.mp4'

pop_limit = 100000

# Plots
fig = plt.figure(figsize=(10.8,10.8), tight_layout=True)
writer = animation.FFMpegWriter(fps=60, bitrate=5000)
with writer.saving(fig, file_name, dpi=100):
  for t in np.arange(start_year, end_year, interval):
    print (str(t))
    plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors,
               compress_pops=False, save_img=False, in_animation=True, show_map = True, show_map_labels = False, show_chart = False)
    writer.grab_frame()

