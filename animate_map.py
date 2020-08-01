import matplotlib.pyplot as plt
from matplotlib import animation

import numpy as np

from static_map import left_align, high_align, low_align
from static_map import pretty_number, pretty_name, pretty_text
from static_map import build_city_data, build_plot_data, plot_chart

cities = build_city_data()

names, pop_fns, lats, longs, colors = build_plot_data(cities)

start_year = 1901
end_year = 2012

compress_pops = False
num_top_cities = 50
interval = 0.06 - 0.001 * num_top_cities
if compress_pops:
  file_name = 'output/animated_' + str(num_top_cities) + '_' + str(start_year) + '_' + str(end_year) + '.mp4'
else:
  file_name = 'output/animated_rel_' + str(num_top_cities) + '_' + str(start_year) + '_' + str(end_year) + '.mp4'

pop_limit = 100000

# Plots
fig = plt.figure(figsize=(19.2,10.8), tight_layout=True)
writer = animation.FFMpegWriter(fps=60, bitrate=5000)
with writer.saving(fig, file_name, dpi=100):
  for t in np.arange(start_year, end_year, interval):
    print (str(t))
    plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors, compress_pops, save_img=False, in_animation=True)
    writer.grab_frame()

