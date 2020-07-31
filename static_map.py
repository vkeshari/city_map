import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm
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

def pretty_name(name):
  if name.strip().endswith("U A"):
    name = name.strip()[:-4].strip()
  elif name.strip().endswith("UA"):
    name = name.strip[:-3].strip()
  else:
    name = name.strip()

  if name == 'Greater Mumbai':
    name = 'Mumbai'
  if name == 'Bruhat Bangalore':
    name = 'Bengaluru'

  return name

def pretty_text(pop, name):
  return pretty_name(name) + ' ' + '(' + pretty_number(pop) + ')'

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

t = 2011
num_chart_cities = 30
map_pop_limit = 100000
label_pop_limit = 200000
max_labels = 12

pops = [interpolate.splev(t, cities[n]['pop'], der=0) for n in names]

top_cities = sorted(zip(pops, names, colors))[-num_chart_cities:]
top_names = [n for _, n, _ in top_cities]
top_pops = [p for p, _, _ in top_cities]
top_colors = [c for _, _, c in top_cities]
top_labels = [pretty_text(p, n) for p, n, _ in top_cities]

show_cities = [(p, n, c, la, lo) for (p, n, c, la, lo) in sorted(zip(pops, names, colors, lats, longs)) if p >= map_pop_limit]
show_pops = [p for p, _, _, _, _ in show_cities]
show_colors = [c for _, _, c, _, _ in show_cities]
show_lats = [la for _, _, _, la, _ in show_cities]
show_longs = [lo for _, _, _, _, lo in show_cities]

label_cities = [(p, n, c, la, lo) for (p, n, c, la, lo) in show_cities if p >= label_pop_limit][-min(len(show_cities), max_labels):]

fig = plt.figure(figsize=(19.2,10.8), tight_layout=True)

map_ax = fig.add_subplot(121)
map_ax.set_title("Map of Cities with Pop. > " + pretty_number(map_pop_limit) + " " +  "(" + str(int(t)) + ")")
m = basemap.Basemap(projection='aeqd', resolution='l',
                    lat_0=20, lon_0=80,
                    llcrnrlat=5, llcrnrlon=68, urcrnrlat=35, urcrnrlon=100)
m.drawlsmask(land_color='white', ocean_color='lightskyblue');
m.drawcountries(linewidth=0.5)
m.scatter(show_longs, show_lats, latlon=True, s=[p/50000 for p in show_pops], alpha=0.5, c=show_colors)
for _, n, _, la, lo in label_cities:
  map_ax.annotate(pretty_name(n), xy = m(lo + 0.5, la - 0.15))

chart_ax = fig.add_subplot(122)
chart_ax.set_title(str(num_chart_cities) + " Largest Cities")
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

plt.show()
#plt.savefig('data/2011_map.png')
