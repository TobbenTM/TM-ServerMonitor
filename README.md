# TM-ServerMonitor

## Overview

This is an app written in python using pygame and requests. It monitors the servers by pinging and fetching websites. It's was meant to be run on my Raspberry Pi and is thus optimized for my setup. Only tested with python 2.6 and it will only work in linux as of now. The reason for using pygame for this sort of thing is because it is the easiest way to make a custom UI wihtout having a window manager.

![What it looks like](http://tobbentm.com/ul/monitor.png "Screenshot of monitor.py")

## Installing

### Requirements

You will need pygame and requests.

Get pygame from aptitude (or [www.pygame.org](http://www.pygame.org)):

	apt-get install python2.6-pygame
	
Get requests from PyPI:

	pip install requests

### Configuration

You will find a "config.py" file with all options. It should be easy enough to figure out what most of it is based on my configuration.

### Running

Run using `python monitor.py`.
Note that on linux you may have to run as root for python to be able to ping.

## Todo

* Implement some kind of statistics for uptime etc.
* Add support for running on Windows.
* Implement SNMP Manager to monitor bandwidth of devices.
* Implement possibility for sound and/or email alerts.

## Known bugs

* It (probably) wont warn when DNS fails unless you restart it.
* May occasionally crash.
* May not detect loss of network.

## License

See LICENSE file.