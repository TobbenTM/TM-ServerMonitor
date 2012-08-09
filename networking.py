# -*- coding: utf-8 -*-

#    Copyright (C) 2012  Tobias Lønnerød Madsen
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Author: TobbenTM 
Email: m@dsen.tv

This is a server-monitoring app built using pygame and requests
Dependecies: pygame & requests
"""

import threading
import time
import os
import requests
from config import *
from array import *

class tcpThread (threading.Thread):
	def __init__(self, ip, sleeptime):
		self.ip = ip
		self.running = True
		self.sleeptime = sleeptime
		self.count = 0
		self.result = ["0.0", "0.0", "0.0", "0.0"]
		self.command = 'ping ' + self.ip
		self.p = os.popen(self.command)
		threading.Thread.__init__(self)
	def run(self):
		while self.running:
			if self.count > 3:
				self.count = 0
			self.line = self.p.readline().split('=')
			if len(self.line[len(self.line)-1][:-4]) < 6:
				self.result[self.count] = self.line[len(self.line)-1][:-4]
			else: 
				self.result[self.count] = 0.0
			#print "array: " + str(self.result)
			self.count += 1
			time.sleep(self.sleeptime)

class httpThread (threading.Thread):
	def __init__(self, target, sleeptime):
		self.target = target
		self.running = True
		self.sleeptime = sleeptime
		self.status = 0
		self.error = 0
		threading.Thread.__init__(self)
	def run(self):
		while self.running:
			try:
				r = requests.get(self.target, timeout=konu_http_timeout)
			except (requests.ConnectionError, requests.Timeout):
				self.status = 504
			except requests.HTTPError:
				self.status = 502
			except Excetion, e:
				self.error = str(e).split(']')[0].split(' ')[1]
			else:
				self.status = r.status_code
			#print "Response received from " + self.target + ": " + str(self.status)
			time.sleep(self.sleeptime)