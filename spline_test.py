f = open('data/city_pops.csv', 'r')
cities = f.readlines()
f.close()

yrs = []
pops = []
for c in cities:
  parts = c.split(',')
  if not 'Greater Mumbai' in parts[0]:
    continue
  yr = 1901
  for p in parts[1:]:
    yrs.append(yr)
    pops.append(eval(p))
    yr += 10

print (yrs)
print (pops)

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

tck = interpolate.splrep(yrs, pops, s=0)
xnew = np.arange(1901, 2011, 0.1)
ynew = interpolate.splev(xnew, tck, der=0)

plt.figure()
plt.plot(yrs, pops, 'x', xnew, ynew, 'b')
plt.legend(['True', 'Cubic Spline'])
plt.axis([1900, 2020, 0, 20000000])
plt.title('Cubic-spline interpolation')
plt.show()

