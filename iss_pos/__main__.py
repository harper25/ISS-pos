from datetime import datetime
import requests
import ephem
from math import degrees
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt # noqa
from mpl_toolkits.basemap import Basemap # noqa
import matplotlib.animation # noqa


req = requests.get("http://www.celestrak.com/NORAD/elements/stations.txt")

tle = req.text.split("\n")[0:3]
line1 = tle[0]
line2 = tle[1]
line3 = tle[2]

iss = ephem.readtle(line1, line2, line3)

fig = plt.figure(figsize=(8, 6), edgecolor='w')

# miller projection
map = Basemap(projection='mill', lon_0=0)

# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60),
                  labels=[0, 0, 0, 1])

# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral', lake_color='aqua')

# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
now = datetime.utcnow()
CS = map.nightshade(now)
text = plt.text(0, 0, 'International\n Space Station')


def animate(i):
    now = datetime.utcnow()
    iss.compute(now)
    lon = degrees(iss.sublong)
    lat = degrees(iss.sublat)

    print("longitude: %f - latitude: %f" % (lon, lat))

    plt.title('Day/Night Map for %s (UTC)' % now.strftime("%d %b %Y %H:%M:%S"))
    x, y = map(lon, lat)
    map.plot(x, y, 'ro', markersize=2)
    text.set_position((x+5, y+5))
    # plt.text(x+5, y+5, 'International\n Space Station')


if __name__ == "__main__":
    ani = matplotlib.animation.FuncAnimation(fig, animate, frames=2,
                                             interval=5000, repeat=True)

    plt.show()


# fig = plt.figure(figsize=(8, 6), edgecolor='w')
# m = Basemap(projection='cyl', resolution=None,
#             llcrnrlat=-90, urcrnrlat=90,
#             llcrnrlon=-180, urcrnrlon=180, )
# draw_map(m)

# python = ">=3.6"
# numpy = "^1.15"
# matplotlib = "^2.0"
# requests = "^2.21"
# pyproj = "^1.9"
# # geos = { path = "../../dep" }

# pyshp = "^2.0"
# pyephem = "^3.7"
