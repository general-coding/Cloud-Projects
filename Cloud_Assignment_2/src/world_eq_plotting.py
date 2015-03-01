'''
Created on Feb 25, 2015

@author: puneeth
'''

import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt 
import numpy as np

# filename = 'earthquake_data.csv'
filename = 'all_month.csv'
 
lats, lons = [], []
magnitudes, timestrings = [], []
with open(filename, 'r', newline='') as f:
    reader = csv.reader(f)
    # ignore header row
    next(reader)
    for row in reader:
#         lats.append(float(row[4]))
#         lons.append(float(row[5]))
#         magnitudes.append(float(row[6]))
#         print(row[3])
#         timestrings.append(row[3])

#         print('lats - ', row[1], 'lons - ', row[2], 'mags - ', row[4], 'times - ', row[3])
        lats.append(float(row[1]))
        lons.append(float(row[2]))
        magnitudes.append(float(row[4]))
        timestrings.append(row[0].replace('T', ',').replace('Z', ' ').strip())
 
# --- Build Map --- 
map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0, lat_0=0, lon_0=-130)
map.drawcoastlines()
map.drawcountries()
# map.fillcontinents(color = 'gray')
map.bluemarble()
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))
 
def get_marker_color(magnitude):
    if magnitude < 3.0:
        return ('go')
    elif magnitude < 5.0:
        return ('yo')
    else:
        return ('ro')
 
# Variable size dots:
#  go through each lat, lon, plot it individually, calculating size dynamically
#  magnitude 1.0 = min dot size; larger quakes scaled by magnitude
count = 0
min_marker_size = 4
for lon, lat, mag in zip(lons, lats, magnitudes):
    count = count + 1
    x,y = map(lon, lat)
    msize = mag * min_marker_size
    marker_string = get_marker_color(mag)
    map.plot(x, y, marker_string, markersize=msize)

print(count)
title_string = "Earthquakes of Magnitude 1.0 or Greater\n"
title_string += "%s through %s" % (timestrings[-1], timestrings[0])
plt.title(title_string)
 
plt.show()