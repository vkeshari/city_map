from matplotlib import pyplot as plt

from build_data import build_city_data, build_plot_data
from plot_data import plot_chart

cities = build_city_data()

names, pop_fns, lats, longs, colors = build_plot_data(cities)

pop_limit = 100000
for num_top_cities in range(10, 60, 10):
  for t in range(1901, 2012, 10):
    # Plots
    fig = plt.figure(figsize=(19.2,10.8), tight_layout=True)
    plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors, compress_pops = False, save_img=True, in_animation=False)

