from datetime import datetime
import requests
import ephem
from math import degrees
import numpy as np
import matplotlib
import matplotlib.animation # noqa
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt # noqa
from mpl_toolkits.basemap import Basemap # noqa


req = requests.get("http://www.celestrak.com/NORAD/elements/stations.txt")

tle = req.text.split("\n")[0:3]
line1 = tle[0]
line2 = tle[1]
line3 = tle[2]

iss_pos = ephem.readtle(line1, line2, line3)

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
map.nightshade(now)

text = plt.text(0, 0, 'International\n Space Station')


def get_current_coords():
    now = datetime.utcnow()
    iss_pos.compute(now)
    lon = degrees(iss_pos.sublong)
    lat = degrees(iss_pos.sublat)
    return lon, lat


def show_route():
    now = datetime.utcnow()
    iss_pos.compute(now)
    pass


def animate(i):
    lon, lat = get_current_coords()
    # print(f'longitude: {lon} - latitude: {lat}')

    plt.title(f'''{datetime.utcnow().strftime("%d %b %Y %H:%M:%S")} UTC
    ISS position: latitude: {lat:.2f}, longitude: {lon:.2f} ''')
    x, y = map(lon, lat)
    map.plot(x, y, 'bo', markersize=2)
    text.set_position((x+5, y+5))


def hello():
    print('Hello!')


def main():
    show_route()
    ani = matplotlib.animation.FuncAnimation(fig, animate, frames=2,
                                             interval=5000, repeat=True)
    plt.show()


if __name__ == "__main__":
    main()
