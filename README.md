# ISS-pos

Track position of International Space Station (ISS) on a map.
The application requests [Celestrak](https://www.celestrak.com/NORAD/documentation/tle-fmt.php) for current ISS orbit data in Two-Line Orbital Element Set Format (TLE), calculates its route and updates its position every 5 seconds.

![](/image/screen.png)

## Installation

* install poetry: `pip install poetry`
* `git clone` the repository
* create a virtual environment, ex.: `virtualenv .venv`
* go inside the virtual environment: `poetry shell`
* install dependencies from `poetry.lock`: `poetry install`

### Mac:

* https://matplotlib.org/basemap/users/installing.html

### Win:

* pyproj -> Win pip install from wheels
* basemap -> Win pip install from wheels
