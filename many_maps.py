from matplotlib import pyplot as plt

from static_map import left_align, high_align, low_align
from static_map import pretty_number, pretty_name, pretty_text
from static_map import build_city_data, build_plot_data, plot_chart

cities = build_city_data()

names, pop_fns, lats, longs, colors = build_plot_data(cities)

pop_limit = 100000
for num_top_cities in range(10, 60, 10):
  for t in range(1901, 2012, 10):
    # Plots
    fig = plt.figure(figsize=(19.2,10.8), tight_layout=True)
    plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors, save_img=True, in_animation=False)

