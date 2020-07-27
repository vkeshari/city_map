import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm, animation
from mpl_toolkits import basemap

import numpy as np
from scipy import interpolate

f = open('data/latlong.csv', 'r')
latlongs = f.readlines()
f.close()

f = open('data/city_pops.csv')
pops = f.readlines()
f.close()

def pretty_number(n):
  cr = n / 10000000
  lk = n / 100000
  th = n / 1000
  if cr >= 1.0:
    ns = "{:.2f}".format(cr) + ' crore'
  elif lk >= 1.0:
    ns = "{:.2f}".format(lk) + ' lakh'
  elif th >= 1.0:
    ns = "{:.2f}".format(th) + ' th'
  else:
    ns = str(pop)
  return ns

def pretty_text(pop, name):
  if name.strip().endswith("U A"):
    name = name.strip()[:-4].strip()
  elif name.strip().endswith("UA"):
    name = name.strip[:-3].strip()
  else:
    name = name.strip()
  s = name + ' ' + '(' + pretty_number(pop) + ')'
  return s

cities = {}
for p in pops[1:]:
  parts = p.split(',')
  cities[parts[0]] = {}
  pop_ts = [t for t in range(1901, 2020, 10)]
  pop_vs = [eval(i) for i in parts[1:]]
  tck = interpolate.splrep(pop_ts, pop_vs, s=0)
  cities[parts[0]]['pop'] = tck
for l in latlongs[1:]:
  parts = l.split(',')
  cities[parts[0]]['lat'] = eval(parts[1])
  cities[parts[0]]['long'] = eval(parts[2])

cmap = cm.get_cmap('brg')
colors = [cmap(i * 1.0 / len(cities)) for i in range(len(cities))]

names = []
lats = []
longs = []
for c in cities:
  names.append(c)
  lats.append(cities[c]['lat'])
  longs.append(cities[c]['long'])

def draw_for_date(t):
  fig.clear()
  pops = [interpolate.splev(t, cities[n]['pop'], der=0) for n in names]

  top_cities = sorted(zip(pops, names, colors))[-25:]
  top_names = [n for _, n, _ in top_cities]
  top_pops = [p for p, _, _ in top_cities]
  top_colors = [c for _, _, c in top_cities]
  top_labels = [pretty_text(p, n) for p, n, _ in top_cities]

  map_ax = fig.add_subplot(121)
  map_ax.set_title("Map of Largest Cities " + "(" + str(int(t)) + ")")
  m = basemap.Basemap(projection='aeqd', resolution='l',
                      lat_0=20, lon_0=80,
                      llcrnrlat=5, llcrnrlon=68, urcrnrlat=35, urcrnrlon=100)
  m.drawlsmask(land_color='white', ocean_color='aqua');
  m.drawcountries(linewidth=0.5)
  m.scatter(longs, lats, latlon=True, s=[p/50000 for p in pops], alpha=0.5, c=colors)

  chart_ax = fig.add_subplot(122)
  chart_ax.set_title("25 Largest Cities")
  chart_ax.spines['right'].set_color('none')
  chart_ax.spines['left'].set_color('none')
  chart_ax.spines['top'].set_color('none')
  chart_ax.spines['bottom'].set_color('none')
  chart_ax.xaxis.set_major_locator(ticker.NullLocator())
  chart_ax.yaxis.set_major_locator(ticker.NullLocator())
  chart_ax.xaxis.set_major_formatter(ticker.NullFormatter())
  chart_ax.xaxis.set_major_formatter(ticker.NullFormatter())
  chart_ax.barh(top_labels, top_pops, alpha = 0.5, color=top_colors)
  for l in top_labels:
    chart_ax.annotate(l, xy=(0, l))

  plt.draw()

FILE_NAME = 'animated.mp4'
fig = plt.figure(figsize=(19.2,10.8))

writer = animation.FFMpegWriter(fps=60, bitrate=5000)
with writer.saving(fig, FILE_NAME, dpi=100):
  for t in np.arange(1901, 2012, 0.01):
    print (str(t))
    draw_for_date(t)
    writer.grab_frame()

