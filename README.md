# cpu-heat-monitor

This project monitors all cpu cores temperature and stores them into a file.
Also a real-time plotter is available.

UPDATE: this only works with **Intel** cpus. With **And Ryzen** does not work and needs a workaround like [this](https://askubuntu.com/questions/1164206/lm-sensors-and-amd-ryzen-x570-chipset).

## Requirements
- *Python 3.x* installed
- *lm-sensors* tool installed:
```console
$ apt install lm-sensors
```
## Usage
To start **monitoring**, execute watch_temperatures script with python:
```console
$ python3 watch_temperatures.py
```
Keep it running and it will show you the average temperature.

To view **real-time** temperatures of this monitor, execute plot_temperatures script with python:
```console
$ python3 plot_temperatures.py
```
This script has a series of arguments:
- **--path**: if no path given, it will check temperatures folder and take the latest file created by watch_temperatures. If path given, he will analyze that file
- **--core**: if you want to view a specific core, set it here. Notice that if you have 8 cores, you can choose between 0 and 7. To show all cores, set -1 or don't use this arg
