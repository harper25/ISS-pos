from datetime import datetime, timedelta
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

text = plt.text(0, 0, 'International\n Space Station', fontweight='bold',
                color='darkblue')

iss_point, = plt.plot([], [], 'ob', markersize=10)


def get_coords(time):
    iss_pos.compute(time)
    lon = degrees(iss_pos.sublong)
    lat = degrees(iss_pos.sublat)
    return lon, lat


def show_route():
    lon_list = []
    lat_list = []
    # ISS part from the past
    for seconds in range(-1000, 1, 10):
        lon, lat = get_coords(datetime.utcnow() + timedelta(seconds=seconds))
        lon_list.append(lon)
        lat_list.append(lat)
    x, y = map(lon_list, lat_list)
    map.plot(x, y, 'or', markersize=2)

    lon_list = []
    lat_list = []
    # ISS part from the future
    for seconds in range(0, 1001, 10):
        lon, lat = get_coords(datetime.utcnow() + timedelta(seconds=seconds))
        lon_list.append(lon)
        lat_list.append(lat)
    x, y = map(lon_list, lat_list)
    map.plot(x, y, 'om', markersize=1)


def animate(i):
    lon, lat = get_coords(datetime.utcnow())
    # print(f'longitude: {lon} - latitude: {lat}')

    plt.title(f'''{datetime.utcnow().strftime("%d %b %Y %H:%M:%S")} UTC
                  ISS position: latitude: {lat:.2f}, longitude: {lon:.2f} ''')
    x, y = map(lon, lat)
    map.plot(x, y, 'or', markersize=2)

    iss_point.set_data(x, y)

    text.set_position((x+5, y+5))

    lon, lat = get_coords(datetime.utcnow() + timedelta(seconds=1000))
    x, y = map(lon, lat)
    map.plot(x, y, 'om', markersize=1)


def main():
    show_route()
    ani = matplotlib.animation.FuncAnimation(fig, animate, frames=2,  # noqa
                                             interval=5000, repeat=True)
    plt.show()


if __name__ == "__main__":
    main()
