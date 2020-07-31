import matplotlib.pyplot as plt
from mpl_toolkits import basemap

fig = plt.figure(figsize=(12, 12), tight_layout=True)
m = basemap.Basemap(projection='aeqd', resolution='l',
                    lat_0=20, lon_0=80,
                    llcrnrlat=5, llcrnrlon=68, urcrnrlat=35, urcrnrlon=100)
m.drawlsmask(land_color='white', ocean_color='lightskyblue');
m.drawcountries(linewidth=0.5)

plt.savefig('data/basemap.png')

