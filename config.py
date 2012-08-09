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

#Config
#__Windows__
#Main window
kon1_title = "TM-Nett"
kon1_subtitle = "Ping-tests"
kon1_p1_title = "vg.no"
kon1_p1_ip = "vg.no"
kon1_p1_limit = 15.0
kon1_p2_title = "Google DNS"
kon1_p2_ip = "8.8.8.8"
kon1_p2_limit = 40.0
kon1_p3_active = True #True/False
kon1_p3_title = "10.13.37.1"
kon1_p3_ip = "10.13.37.1"
kon1_p3_limit = 1.0
kon1_p4_active = True #True/False
kon1_p4_title = "10.13.37.50"
kon1_p4_ip = "10.13.37.50"
kon1_p4_limit = 1.0
#Window3
kon3_title = "TM-Debian"
kon3_subtitle = "10.13.37.6"
kon3_ip = "10.13.37.6"
kon3_limit = 1.0 #ms ping limit to begin warns
kon3_dn = "http://" + "10.13.37.6"
#Window4
kon4_title = "TM-Winserver"
kon4_subtitle = "10.13.37.5"
kon4_ip = "10.13.37.5"
kon4_limit = 1.0
#Window5
kon5_title = "ESXi Server"
kon5_subtitle = "10.13.37.4"
kon5_ip = "10.13.37.4"
kon5_limit = 1.0
#Window6
kon6_title = "Linode"
kon6_subtitle = "109.74.195.196"
kon6_ip = "109.74.195.196"
kon6_limit = 55.0
kon6_dn = "http://" + "dsen.tv"
#__Universal__
konu_web = "Apache"
konu_ping = "Ping"
konu_ok = "OK"
konu_warn = "WARN"
konu_fail = "FAIL"
#Settings
konu_sound_enabled = False #Inactive
konu_windowtitle = "TM-ServerMonitor"
konu_font = None # None for system font. To use other font put it in root directory and enter full name here. ex: "Roboto-Regular.ttf". Protip: Roboto Regular works pretty sweet.
konu_fontsize = 0 # Used to incease/decrease font size. Kan be a negative number. ex: -1
konu_resolution = (1280, 1024)
konu_fullscreen = True
konu_mouse_visible = 0 # 1 = On, 0 = Off
konu_time_format = "%H:%M:%S" #Refer to http://docs.python.org/library/time.html#time.strftime to see options
konu_date_format = "%d.%m.%Y" #Refer to http://docs.python.org/library/time.html#time.strftime to see options
konu_fps = 5
konu_tcp_sleep = 5
konu_http_sleep = 10
konu_http_timeout = 2.0
#Colors
color_white = (255, 255, 255)
color_green = (12, 199, 26)
color_yellow = (230, 228, 22)
color_red = (201, 8, 8)