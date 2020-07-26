import geopy

geo = geopy.geocoders.Nominatim(user_agent="city_map_keshari")

def get_lat_long(c):
  gcode = geo.geocode(c + ' india')
  if gcode is None:
    print ('\t' + "[FAIL]" + '\t' + c)
    return (0, 0)
  return (gcode.latitude, gcode.longitude)
  

f = open('data/city_pops.csv', 'r')
cities = f.readlines()
f.close()

f = open('data/latlong.csv', 'w')
f.write('city,lat,long\n')
for c in cities[1:]:
  parts = c.split(',')
  if parts[0].endswith('U A'):
    city_name = parts[0][:-4]
  elif parts[0].endswith('UA'):
    city_name = parts[0][:-3]
  else:
    city_name = parts[0]
  print (parts[0])
  print (city_name)
  (latitude, longitude) = get_lat_long(city_name)
  print ('\t' + str(latitude) + '\t' + str(longitude))
  f.write(parts[0] + ',' + str(latitude) + ',' + str(longitude) + '\n')
f.close()
  
