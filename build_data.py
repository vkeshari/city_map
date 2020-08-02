from matplotlib import cm
from scipy import interpolate

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

