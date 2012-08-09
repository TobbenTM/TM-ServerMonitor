# TM-ServerMonitor

## Overview

This is an app written in python using pygame and requests. It's was meant to be run on my Raspberry Pi and is thus optimized for my setup. Only tested with python 2.6 and it will only work in linux as of now.

## Installing

### Requirements

You will need pygame and requests.

Get pygame from aptitude (or [www.pygame.org](http://www.pygame.org)):

	apt-get install python2.6-pygame
	
Get requests from PyPI:

	pip install requests

### Configuration

You will find a "config.py" file with all options. It should be easy enough to figure out what most of it is.

## Todo

* Implement some kind of statistics for uptime etc.
* Ass support for running on Windows.
* Implement SNMP Manager to monitor bandwidth of devices.

## License

See LICENSE file.