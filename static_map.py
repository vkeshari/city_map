import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm
from mpl_toolkits import basemap

import math
import numpy as np
from scipy import interpolate

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
  if name.strip().endswith("U  A"):
    name = name.strip()[:-5].strip()
  elif name.strip().endswith("U A"):
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

# Special labal alignment on map to reduce clutter
left_align = set(['Srinagar', 'Amritsar', 'Ludhiana', 'Delhi', 'Faridabad', 'Jaipur', 'Jodhpur',
                  'Bikaner', 'Gwalior', 'Aligarh', 'Allahabad', 'Dhanbad', 'Ranchi', 'Jamshedpur',
                  'Ahmadabad', 'Rajkot', 'Bhavnagar', 'Bhopal', 'Nashik', 'Surat', 'Mumbai',
                  'Kolhapur', 'Nagpur', 'Hyderabad', 'Bengaluru', 'Kozhikode', 'Kannur',
                  'Thrissur', 'Kochi', 'Kollam', 'Thiruvananthapuram'])
high_align = set(['Meerut', 'Dehradun', 'Lucknow', 'Patna', 'Jaipur', 'Dhanbad', 'Bhopal', 'Jalandhar', 'Nashik',
                  'Aurangabad', 'Raipur', 'Malappuram', 'Kollam', 'Tiruchirappalli'])
low_align = set(['Allahabad', 'Gwalior', 'Faridabad', 'Moradabad', 'Bareilly', 'Shahjahanpur', 'Kanpur', 'Varanasi', 'Gaya', 'Jamshedpur', 'Vadodara',
                 'Durg Bhilai', 'Hyderabad', 'Robertsonpet', 'Coimbatore', 'Guntur', 'Thiruvananthapuram'])

def build_city_data():
  f = open('data/latlong.csv', 'r')
  latlongs = f.readlines()
  f.close()

  f = open('data/city_pops.csv')
  pops = f.readlines()
  f.close()

  # Build city data by time
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

  return cities

cities = build_city_data()

def build_plot_data(cities):
  # Assign colors to each city
  cmap = cm.get_cmap('brg')
  colors = [cmap(i * 1.0 / len(cities)) for i in range(len(cities))]

  # Arrays to plot
  names = []
  lats = []
  longs = []
  pop_fns = []
  for c in cities:
    names.append(c)
    lats.append(cities[c]['lat'])
    longs.append(cities[c]['long'])
    pop_fns.append(cities[c]['pop'])

  return names, pop_fns, lats, longs, colors

names, pop_fns, lats, longs, colors = build_plot_data(cities)

def plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors, compress_pops, save_img, in_animation):
  assert t >= 1901, "t (year) must be >= 1901"
  assert t < 2012, "t (year) must be < 2012"

  assert num_top_cities >= 10, "num_top_cities must be >= 10"
  assert num_top_cities <= 50, "num_top_cities must be <= 50"

  assert pop_limit >= 100000, "pop_limit must be >= 1,00,000"
  assert pop_limit <= 20000000, "pop_limit must be <= 2,00,00,000"
  
  if in_animation:
    assert not save_img, "save_img cannot be True if in_animation is True"

  if in_animation:
    fig.clear()

  map_pop_limit = pop_limit
  label_pop_limit = pop_limit
  max_labels = num_top_cities
  num_chart_cities = num_top_cities

  chart_text_size = 22.5 - 0.25 * num_chart_cities
  map_text_size = 22.5 - 0.25 * max_labels

  # Population at time t
  pops = [interpolate.splev(t, pop_fn, der=0) for pop_fn in pop_fns]

  # Top cities to show in chart
  top_cities = sorted(zip(pops, names, colors))[-num_chart_cities:]
  top_names = [n for _, n, _ in top_cities]
  top_pops = [p for p, _, _ in top_cities]
  top_colors = [c for _, _, c in top_cities]
  top_labels = [pretty_text(p, n) for p, n, _ in top_cities]

  # Cities to show on map
  show_cities = [(p, n, c, la, lo) for (p, n, c, la, lo) in sorted(zip(pops, names, colors, lats, longs)) if p >= map_pop_limit]
  show_pops = [p for p, _, _, _, _ in show_cities]
  show_colors = [c for _, _, c, _, _ in show_cities]
  show_lats = [la for _, _, _, la, _ in show_cities]
  show_longs = [lo for _, _, _, _, lo in show_cities]

  # Labels to show on map
  label_cities = [(p, n, c, la, lo) for (p, n, c, la, lo) in show_cities if p >= label_pop_limit][-min(len(show_cities), max_labels):]

  # Basemap
  map_ax = fig.add_subplot(121)
  map_ax.set_title("Map of Cities with Pop. > " + pretty_number(map_pop_limit) + " " +  "(" + str(int(t)) + ")", size = map_text_size)
  m = basemap.Basemap(projection='aeqd', resolution='l',
                      lat_0=20, lon_0=80,
                      llcrnrlat=5, llcrnrlon=68, urcrnrlat=35, urcrnrlon=100)
  m.drawlsmask(land_color='white', ocean_color='lightskyblue');
  m.drawcountries(linewidth=0.5)

  # Show cities on map
  m.scatter(show_longs, show_lats, latlon=True, s=[p/50000 for p in show_pops], alpha=0.5, c=show_colors)

  # Show labels on map
  for p, n, _, la, lo in label_cities:
    label_name = pretty_name(n)
    if label_name in left_align:
      ha = 'right'
      lo_adjust = -math.sqrt(p)/8000
    else:
      ha = 'left'
      lo_adjust = math.sqrt(p)/8000
    if label_name in low_align:
      va = 'top'
    elif label_name in high_align:
      va = 'bottom'
    else:
      va = 'center'
    map_ax.annotate(label_name, xy = m(lo + lo_adjust, la), va = va, ha = ha, size = map_text_size)

  # Show chart
  chart_ax = fig.add_subplot(122)
  chart_ax.set_title(str(num_chart_cities) + " Largest Cities", size = chart_text_size)
  chart_ax.spines['right'].set_color('none')
  chart_ax.spines['left'].set_color('none')
  chart_ax.spines['top'].set_color('none')
  chart_ax.spines['bottom'].set_color('none')
  chart_ax.xaxis.set_major_locator(ticker.NullLocator())
  chart_ax.yaxis.set_major_locator(ticker.NullLocator())
  chart_ax.xaxis.set_major_formatter(ticker.NullFormatter())
  chart_ax.xaxis.set_major_formatter(ticker.NullFormatter())
  if compress_pops:
    chart_ax.set_xlim(0, 20000000)
  chart_ax.barh(top_labels, top_pops, alpha = 0.5, color=top_colors)
  for l in top_labels:
    chart_ax.annotate(l, xy=(0.1, l), va = 'center', size = chart_text_size)

  if in_animation:
    plt.draw()
  else:
    if save_img:
      plt.savefig('output/' + 'map_' + str(num_top_cities) + '_' + str(t) + '.png')
    else:
      plt.show()

# Plot parameters
t = 2011
pop_limit = 100000
num_top_cities = 50
save_img = False

# Plots
fig = plt.figure(figsize=(19.2,10.8), tight_layout=True)

plot_chart(fig, t, num_top_cities, pop_limit, names, pop_fns, lats, longs, colors, compress_pops = False, save_img = save_img, in_animation = False)

