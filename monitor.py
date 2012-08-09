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


import os, pygame, time
from networking import *
from config import *
from pygame.locals import *

def main():
	#init
	pygame.init()
	if konu_fullscreen == True:
		screen = pygame.display.set_mode(konu_resolution, pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(konu_resolution)
	pygame.display.set_caption(konu_windowtitle)
	pygame.mouse.set_visible(konu_mouse_visible)
		
	#Threads
	tcp1_1 = tcpThread(kon1_p1_ip, konu_tcp_sleep)
	tcp1_1.setDaemon(True)
	tcp1_2 = tcpThread(kon1_p2_ip, konu_tcp_sleep)
	tcp1_2.setDaemon(True)
	if kon1_p3_active:
		tcp1_3 = tcpThread(kon1_p3_ip, konu_tcp_sleep)
		tcp1_3.setDaemon(True)
	if kon1_p4_active:
		tcp1_4 = tcpThread(kon1_p4_ip, konu_tcp_sleep)
		tcp1_4.setDaemon(True)
	tcp3 = tcpThread(kon3_ip, konu_tcp_sleep)
	tcp3.setDaemon(True)
	tcp4 = tcpThread(kon4_ip, konu_tcp_sleep)
	tcp4.setDaemon(True)
	tcp5 = tcpThread(kon5_ip, konu_tcp_sleep)
	tcp5.setDaemon(True)
	tcp6 = tcpThread(kon6_ip, konu_tcp_sleep)
	tcp6.setDaemon(True)
	
	http3 = httpThread(kon3_dn, konu_http_sleep)
	http3.setDaemon(True)
	http6 = httpThread(kon6_dn, konu_http_sleep)
	http6.setDaemon(True)
	
	tcp1_1.start()
	tcp1_2.start()
	if kon1_p3_active:
		tcp1_3.start()
	if kon1_p4_active:
		tcp1_4.start()
	tcp3.start()
	tcp4.start()
	tcp5.start()
	tcp6.start()
	
	http3.start()
	http6.start()
	
	#Coords
	quarterw = screen.get_width()/12
	
	hcenter1 = quarterw*2
	hcenter1v = quarterw
	hcenter1h = quarterw*3
	hcenter2 = hcenter1*3
	hcenter2v = hcenter2-quarterw
	hcenter2h = hcenter2+quarterw
	hcenter3 = hcenter1*5
	hcenter3v = hcenter3-quarterw
	hcenter3h = hcenter3+quarterw
	
	vcenter = screen.get_height()/2
	
	#Background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	
	#Dividers
	div_center_hor = pygame.Surface((screen.get_width(), 1))
	div_center_hor = div_center_hor.convert()
	div_center_hor.fill((color_white))
	
	div_right_ver = pygame.Surface((1, screen.get_height()))
	div_right_ver = div_right_ver.convert()
	div_right_ver.fill((color_white))

	div_left_ver = pygame.Surface((1, screen.get_height()/2))
	div_left_ver = div_left_ver.convert()
	div_left_ver.fill((color_white))
	
	div_main_1 = pygame.Surface((quarterw*4, 1))
	div_main_1 = div_main_1.convert()
	div_main_1.fill((color_white))
	
	#Fonts
	small_font = pygame.font.Font(konu_font, 18 + konu_fontsize)
	normal_font = pygame.font.Font(konu_font, 30 + konu_fontsize)
	big_font = pygame.font.Font(konu_font, 48 + konu_fontsize)
	xl_font = pygame.font.Font(konu_font, 60 + konu_fontsize)
	xxl_font = pygame.font.Font(konu_font, 80 + konu_fontsize)
	
	#Utils
	def checkMS(ms, limit):
		if ms == 0.0:
			return color_red
		elif ms < limit:
			return color_green
		elif ms >= limit:
			return color_yellow
		else:
			return color_red
	
	def checkArray(type, sarray, limit):
		array = [float(i) for i in sarray]
		high = array[0]
		low = array[0]
		for ms in array[1:]:
			if ms > high:
				high = ms
			if ms < low:
				low = ms
		
		if type == "color":
			if high == 0.0 and low == 0.0:
				return color_red
			elif high < limit and low > 0.0:
				return color_green
			elif high >= limit or low == 0.0:
				return color_yellow
			else:
				return color_red
		elif type == "text":
			if high == 0.0 and low == 0.0:
				return konu_fail
			elif high < limit and low > 0.0:
				return konu_ok
			elif high >= limit or low == 0.0:
				return konu_warn
			else:
				return konu_fail
		elif type == "debug":
			print "high: " + str(high) + ". low: " + str(low)
		else:
			print "Returned none"
			return
		
	
	def killAll():
		tcp1_1.running = False
		tcp1_2.running = False
		if kon1_p3_active:
			tcp1_3.running = False
		if kon1_p4_active:
			tcp1_4.running = False
		tcp3.running = False
		tcp4.running = False
		tcp5.running = False
		tcp6.running = False
		
		http3.running = False
		http6.running = False
	
	clock = pygame.time.Clock()

	while 1:
		clock.tick(konu_fps)
		
		#print "Start loop"
		
		#Handle Input Events
		for event in pygame.event.get():
				if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
					killAll()
					return
			
		#____Variables____
		var_time = time.strftime(konu_time_format)
		var_date = time.strftime(konu_date_format)
		
		#____Background stuff____
		screen.blit(background, (0, 0))
		screen.blit(div_center_hor, (0, vcenter))
		screen.blit(div_right_ver, (screen.get_width()/3*2, 0))
		screen.blit(div_left_ver, (screen.get_width()/3, vcenter))
		fps_text = small_font.render("FPS: %.2f" % clock.get_fps(), 1, (color_white))
		screen.blit(fps_text, (5, screen.get_height()-5-fps_text.get_height()))
		
		#**Main Window**
		#Titles
		w1_title = xl_font.render(kon1_title, 1, (color_white))
		screen.blit(w1_title, (hcenter1 - w1_title.get_width()/2, 10))
		w1_subtitle = normal_font.render(kon1_subtitle, 1, (color_white))
		screen.blit(w1_subtitle, (quarterw/2+div_main_1.get_width()/2-w1_subtitle.get_width()/2 ,150-3-w1_subtitle.get_height()))
		
		#Date/time
		time_text = normal_font.render(str(var_time), 1, (color_white))
		date_text = normal_font.render(str(var_date), 1, (color_white))
		screen.blit(time_text, (hcenter2 - time_text.get_width()/2, 10))
		screen.blit(date_text, (hcenter2 - date_text.get_width()/2, 45))
		
		#Divider
		screen.blit(div_main_1, (quarterw/2, 150))
		
		#Ping tests
		#Ping1
		w1_p1_title = normal_font.render(kon1_p1_title, 1, (color_white))
		screen.blit(w1_p1_title, (quarterw*1.5-w1_p1_title.get_width()/2, 150+2))
		w1_p1_pings = xl_font.render(checkArray("text", tcp1_1.result, kon1_p1_limit), 1, checkArray("color", tcp1_1.result, kon1_p1_limit))
		screen.blit(w1_p1_pings, (quarterw*1.5 - w1_p1_pings.get_width()/2, 175))
		w1_p1_pingms1 = small_font.render(str(tcp1_1.result[0])+"ms", 1, (checkMS(float(tcp1_1.result[0]), kon1_p1_limit)))
		screen.blit(w1_p1_pingms1, (quarterw*1.5 - w1_p1_pingms1.get_width()/2, 175+w1_p1_pings.get_height()-5))
		w1_p1_pingms2 = small_font.render(str(tcp1_1.result[1])+"ms", 1, (checkMS(float(tcp1_1.result[1]), kon1_p1_limit)))
		screen.blit(w1_p1_pingms2, (quarterw*1.5 -  w1_p1_pingms2.get_width()/2, 175+w1_p1_pings.get_height()+w1_p1_pingms1.get_height()-5))
		w1_p1_pingms3 = small_font.render(str(tcp1_1.result[2])+"ms", 1, (checkMS(float(tcp1_1.result[2]), kon1_p1_limit)))
		screen.blit(w1_p1_pingms3, (quarterw*1.5 - w1_p1_pingms3.get_width()/2, 175+w1_p1_pings.get_height()+w1_p1_pingms1.get_height()*2-5))
		w1_p1_pingms4 = small_font.render(str(tcp1_1.result[3])+"ms", 1, (checkMS(float(tcp1_1.result[3]), kon1_p1_limit)))
		screen.blit(w1_p1_pingms4, (quarterw*1.5 - w1_p1_pingms4.get_width()/2, 175+w1_p1_pings.get_height()+w1_p1_pingms1.get_height()*3-5))
		
		#Ping2
		w1_p2_title = normal_font.render(kon1_p2_title, 1, (color_white))
		screen.blit(w1_p2_title, (quarterw*3.5-w1_p2_title.get_width()/2, 150+2))
		w1_p2_pings = xl_font.render(checkArray("text", tcp1_2.result, kon1_p2_limit), 1, checkArray("color", tcp1_2.result, kon1_p2_limit))
		screen.blit(w1_p2_pings, (quarterw*3.5 - w1_p2_pings.get_width()/2, 175))
		w1_p2_pingms1 = small_font.render(str(tcp1_2.result[0])+"ms", 1, (checkMS(float(tcp1_2.result[0]), kon1_p2_limit)))
		screen.blit(w1_p2_pingms1, (quarterw*3.5 - w1_p2_pingms1.get_width()/2, 175+w1_p2_pings.get_height()-5))
		w1_p2_pingms2 = small_font.render(str(tcp1_2.result[1])+"ms", 1, (checkMS(float(tcp1_2.result[1]), kon1_p2_limit)))
		screen.blit(w1_p2_pingms2, (quarterw*3.5 -  w1_p2_pingms2.get_width()/2, 175+w1_p2_pings.get_height()+w1_p2_pingms1.get_height()-5))
		w1_p2_pingms3 = small_font.render(str(tcp1_2.result[2])+"ms", 1, (checkMS(float(tcp1_2.result[2]), kon1_p2_limit)))
		screen.blit(w1_p2_pingms3, (quarterw*3.5 - w1_p2_pingms3.get_width()/2, 175+w1_p2_pings.get_height()+w1_p2_pingms1.get_height()*2-5))
		w1_p2_pingms4 = small_font.render(str(tcp1_2.result[3])+"ms", 1, (checkMS(float(tcp1_2.result[3]), kon1_p2_limit)))
		screen.blit(w1_p2_pingms4, (quarterw*3.5 - w1_p2_pingms4.get_width()/2, 175+w1_p2_pings.get_height()+w1_p2_pingms1.get_height()*3-5))
		
		#Ping3
		if kon1_p3_active:
			w1_p3_title = normal_font.render(kon1_p3_title, 1, (color_white))
			screen.blit(w1_p3_title, (quarterw*1.5-w1_p3_title.get_width()/2, 150+2+175))
			w1_p3_pings = xl_font.render(checkArray("text", tcp1_3.result, kon1_p3_limit), 1, checkArray("color", tcp1_3.result, kon1_p3_limit))
			screen.blit(w1_p3_pings, (quarterw*1.5 - w1_p3_pings.get_width()/2, 175+175))
			w1_p3_pingms1 = small_font.render(str(tcp1_3.result[0])+"ms", 1, (checkMS(float(tcp1_3.result[0]), kon1_p3_limit)))
			screen.blit(w1_p3_pingms1, (quarterw*1.5 - w1_p3_pingms1.get_width()/2, 175+w1_p3_pings.get_height()-5+175))
			w1_p3_pingms2 = small_font.render(str(tcp1_3.result[1])+"ms", 1, (checkMS(float(tcp1_3.result[1]), kon1_p3_limit)))
			screen.blit(w1_p3_pingms2, (quarterw*1.5 -  w1_p3_pingms2.get_width()/2, 175+w1_p3_pings.get_height()+w1_p3_pingms1.get_height()-5+175))
			w1_p3_pingms3 = small_font.render(str(tcp1_3.result[2])+"ms", 1, (checkMS(float(tcp1_3.result[2]), kon1_p3_limit)))
			screen.blit(w1_p3_pingms3, (quarterw*1.5 - w1_p3_pingms3.get_width()/2, 175+w1_p3_pings.get_height()+w1_p3_pingms1.get_height()*2-5+175))
			w1_p3_pingms4 = small_font.render(str(tcp1_3.result[3])+"ms", 1, (checkMS(float(tcp1_3.result[3]), kon1_p3_limit)))
			screen.blit(w1_p3_pingms4, (quarterw*1.5 - w1_p3_pingms4.get_width()/2, 175+w1_p3_pings.get_height()+w1_p3_pingms1.get_height()*3-5+175))
			
		#Ping4
		if kon1_p4_active:
			w1_p4_title = normal_font.render(kon1_p4_title, 1, (color_white))
			screen.blit(w1_p4_title, (quarterw*3.5-w1_p4_title.get_width()/2, 150+2+175))
			w1_p4_pings = xl_font.render(checkArray("text", tcp1_4.result, kon1_p4_limit), 1, checkArray("color", tcp1_4.result, kon1_p4_limit))
			screen.blit(w1_p4_pings, (quarterw*3.5 - w1_p4_pings.get_width()/2, 175+175))
			w1_p4_pingms1 = small_font.render(str(tcp1_4.result[0])+"ms", 1, (checkMS(float(tcp1_4.result[0]), kon1_p4_limit)))
			screen.blit(w1_p4_pingms1, (quarterw*3.5 - w1_p4_pingms1.get_width()/2, 175+w1_p4_pings.get_height()-5+175))
			w1_p4_pingms2 = small_font.render(str(tcp1_4.result[1])+"ms", 1, (checkMS(float(tcp1_4.result[1]), kon1_p4_limit)))
			screen.blit(w1_p4_pingms2, (quarterw*3.5 -  w1_p4_pingms2.get_width()/2, 175+w1_p4_pings.get_height()+w1_p4_pingms1.get_height()-5+175))
			w1_p4_pingms3 = small_font.render(str(tcp1_4.result[2])+"ms", 1, (checkMS(float(tcp1_4.result[2]), kon1_p4_limit)))
			screen.blit(w1_p4_pingms3, (quarterw*3.5 - w1_p4_pingms3.get_width()/2, 175+w1_p4_pings.get_height()+w1_p4_pingms1.get_height()*2-5+175))
			w1_p4_pingms4 = small_font.render(str(tcp1_4.result[3])+"ms", 1, (checkMS(float(tcp1_4.result[3]), kon1_p4_limit)))
			screen.blit(w1_p4_pingms4, (quarterw*3.5 - w1_p4_pingms4.get_width()/2, 175+w1_p4_pings.get_height()+w1_p4_pingms1.get_height()*3-5+175))
		
		#**Window3**
		#Titles
		w3_title = normal_font.render(kon3_title, 1, (color_white))
		w3_subtitle = normal_font.render(kon3_subtitle, 1, (color_white))
		screen.blit(w3_title, (hcenter3 - w3_title.get_width()/2, 10))
		screen.blit(w3_subtitle, (hcenter3 - w3_subtitle.get_width()/2, 45))
		
		#Monitors
		w3_pingt = normal_font.render(konu_ping, 1, (color_white))
		w3_apachet = normal_font.render(konu_web, 1, (color_white))
		screen.blit(w3_pingt, (hcenter3v - w3_pingt.get_width()/2, 120))
		screen.blit(w3_apachet, (hcenter3h - w3_apachet.get_width()/2, 120))
		
		#Stats
		w3_pings = xl_font.render(checkArray("text", tcp3.result, kon3_limit), 1, checkArray("color", tcp3.result, kon3_limit))
		screen.blit(w3_pings, (hcenter3v - w3_pings.get_width()/2, 190 - w3_pings.get_height()/2))
		w3_pingms1 = small_font.render(str(tcp3.result[0])+"ms", 1, (checkMS(float(tcp3.result[0]), kon3_limit)))
		screen.blit(w3_pingms1, (hcenter3 + 7 - w3_pingms1.get_width()/2, 150))
		w3_pingms2 = small_font.render(str(tcp3.result[1])+"ms", 1, (checkMS(float(tcp3.result[1]), kon3_limit)))
		screen.blit(w3_pingms2, (hcenter3 + 7 - w3_pingms2.get_width()/2, 170))
		w3_pingms3 = small_font.render(str(tcp3.result[2])+"ms", 1, (checkMS(float(tcp3.result[2]), kon3_limit)))
		screen.blit(w3_pingms3, (hcenter3 + 7 - w3_pingms3.get_width()/2, 190))
		w3_pingms4 = small_font.render(str(tcp3.result[3])+"ms", 1, (checkMS(float(tcp3.result[3]), kon3_limit)))
		screen.blit(w3_pingms4, (hcenter3 + 7 - w3_pingms4.get_width()/2, 210))
		if http3.error == 0:
			if http3.status == 0 or http3.status == 404:
				w3_apaches = big_font.render(konu_warn, 1, (color_yellow))
				screen.blit(w3_apaches, (hcenter3h - w3_apaches.get_width()/2, 190 - w3_apaches.get_height()/2))
			elif http3.status == 200:
				w3_apaches = xxl_font.render(konu_ok, 1, (color_green))
				screen.blit(w3_apaches, (hcenter3h - w3_apaches.get_width()/2, 190 - w3_apaches.get_height()/2))
			else:
				print "http3 status: ", http3.status
				w3_apaches = xl_font.render(konu_fail, 1, (color_red))
				screen.blit(w3_apaches, (hcenter3h - w3_apaches.get_width()/2, 185 - w3_apaches.get_height()/2))
				w3_err = small_font.render("status: " + str(http3.status), 1, (color_red))
				screen.blit(w3_err, (hcenter3h - w3_err.get_width()/2, 215 - w3_err.get_height()/2))
		else: 
			print "http3 error: ", http3.error
			w3_apaches = xl_font.render(konu_fail, 1, (color_red))
			screen.blit(w3_apaches, (hcenter3h - w3_apaches.get_width()/2, 185 - w3_apaches.get_height()/2))
			w3_err = small_font.render("error: " + str(http3.error), 1, (color_red))
			screen.blit(w3_err, (hcenter3h - w3_err.get_width()/2, 215 - w3_err.get_height()/2))
			
		#**Window4**
		#Titles
		w4_title = normal_font.render(kon4_title, 1, (color_white))
		w4_subtitle = normal_font.render(kon4_subtitle, 1, (color_white))
		screen.blit(w4_title, (hcenter1 - w4_title.get_width()/2, vcenter + 10))
		screen.blit(w4_subtitle, (hcenter1 - w4_subtitle.get_width()/2, vcenter + 45))
		
		#Monitors
		w4_pingt = normal_font.render(konu_ping, 1, (color_white))
		screen.blit(w4_pingt, (hcenter1v - w4_pingt.get_width()/2 + 20, vcenter + 120))
		
		#Stats
		w4_pings = xxl_font.render(checkArray("text", tcp4.result, kon4_limit), 1, checkArray("color", tcp4.result, kon4_limit))
		screen.blit(w4_pings, (hcenter1v - w4_pings.get_width()/2 + 20, vcenter + 190 - w4_pings.get_height()/2))
		w4_pingms1 = normal_font.render(str(tcp4.result[0])+"ms", 1, (checkMS(float(tcp4.result[0]), kon4_limit)))
		screen.blit(w4_pingms1, (hcenter1h - w4_pingms1.get_width()/2, vcenter + 130))
		w4_pingms2 = normal_font.render(str(tcp4.result[1])+"ms", 1, (checkMS(float(tcp4.result[1]), kon4_limit)))
		screen.blit(w4_pingms2, (hcenter1h - w4_pingms2.get_width()/2, vcenter + 162))
		w4_pingms3 = normal_font.render(str(tcp4.result[2])+"ms", 1, (checkMS(float(tcp4.result[2]), kon4_limit)))
		screen.blit(w4_pingms3, (hcenter1h - w4_pingms3.get_width()/2, vcenter + 194))
		w4_pingms4 = normal_font.render(str(tcp4.result[3])+"ms", 1, (checkMS(float(tcp4.result[3]), kon4_limit)))
		screen.blit(w4_pingms4, (hcenter1h - w4_pingms4.get_width()/2, vcenter + 224))
		
		#**Window5**
		#Titles
		w5_title = normal_font.render(kon5_title, 1, (color_white))
		w5_subtitle = normal_font.render(kon5_subtitle, 1, (color_white))
		screen.blit(w5_title, (hcenter2 - w5_title.get_width()/2, vcenter + 10))
		screen.blit(w5_subtitle, (hcenter2 - w5_subtitle.get_width()/2, vcenter + 45))
		
		#Monitors
		w5_pingt = normal_font.render(konu_ping, 1, (color_white))
		screen.blit(w5_pingt, (hcenter2v - w5_pingt.get_width()/2 + 20, vcenter + 120))
		
		#Stats
		w5_pings = xxl_font.render(checkArray("text", tcp5.result, kon5_limit), 1, checkArray("color", tcp5.result, kon5_limit))
		screen.blit(w5_pings, (hcenter2v - w5_pings.get_width()/2 + 20, vcenter + 190 - w5_pings.get_height()/2))
		w5_pingms1 = normal_font.render(str(tcp5.result[0])+"ms", 1, (checkMS(float(tcp5.result[0]), kon5_limit)))
		screen.blit(w5_pingms1, (hcenter2h - w5_pingms1.get_width()/2, vcenter + 130))
		w5_pingms2 = normal_font.render(str(tcp5.result[1])+"ms", 1, (checkMS(float(tcp5.result[1]), kon5_limit)))
		screen.blit(w5_pingms2, (hcenter2h - w5_pingms2.get_width()/2, vcenter + 162))
		w5_pingms3 = normal_font.render(str(tcp5.result[2])+"ms", 1, (checkMS(float(tcp5.result[2]), kon5_limit)))
		screen.blit(w5_pingms3, (hcenter2h - w5_pingms3.get_width()/2, vcenter + 194))
		w5_pingms4 = normal_font.render(str(tcp5.result[3])+"ms", 1, (checkMS(float(tcp5.result[3]), kon5_limit)))
		screen.blit(w5_pingms4, (hcenter2h - w5_pingms4.get_width()/2, vcenter + 224))
		
		#**Window6**
		#Titles
		w6_title = normal_font.render(kon6_title, 1, (color_white))
		w6_subtitle = normal_font.render(kon6_subtitle, 1, (color_white))
		screen.blit(w6_title, (hcenter3 - w6_title.get_width()/2, vcenter + 10))
		screen.blit(w6_subtitle, (hcenter3 - w6_subtitle.get_width()/2, vcenter + 45))
		
		#Monitors
		w6_pingt = normal_font.render(konu_ping, 1, (color_white))
		w6_apachet = normal_font.render(konu_web, 1, (color_white))
		screen.blit(w6_pingt, (hcenter3v - w6_pingt.get_width()/2, vcenter + 120))
		screen.blit(w6_apachet, (hcenter3h - w6_apachet.get_width()/2, vcenter + 120))
		
		#Stats
		w6_pings = xl_font.render(checkArray("text", tcp6.result, kon6_limit), 1, checkArray("color", tcp6.result, kon6_limit))
		screen.blit(w6_pings, (hcenter3v - w6_pings.get_width()/2, vcenter + 190 - w6_pings.get_height()/2))
		w6_pingms1 = small_font.render(str(tcp6.result[0])+"ms", 1, (checkMS(float(tcp6.result[0]), kon6_limit)))
		screen.blit(w6_pingms1, (hcenter3 + 7 - w6_pingms1.get_width()/2, vcenter + 150))
		w6_pingms2 = small_font.render(str(tcp6.result[1])+"ms", 1, (checkMS(float(tcp6.result[1]), kon6_limit)))
		screen.blit(w6_pingms2, (hcenter3 + 7 - w6_pingms2.get_width()/2, vcenter + 170))
		w6_pingms3 = small_font.render(str(tcp6.result[2])+"ms", 1, (checkMS(float(tcp6.result[2]), kon6_limit)))
		screen.blit(w6_pingms3, (hcenter3 + 7 - w6_pingms3.get_width()/2, vcenter + 190))
		w6_pingms4 = small_font.render(str(tcp6.result[3])+"ms", 1, (checkMS(float(tcp6.result[3]), kon6_limit)))
		screen.blit(w6_pingms4, (hcenter3 + 7 - w6_pingms4.get_width()/2, vcenter + 210))
		if http6.error == 0:
			if http6.status == 0 or http6.status == 404:
				w6_apaches = big_font.render(konu_warn, 1, (color_yellow))
				screen.blit(w6_apaches, (hcenter3h - w6_apaches.get_width()/2, vcenter + 190 - w6_apaches.get_height()/2))
			elif http6.status == 200:
				w6_apaches = xxl_font.render(konu_ok, 1, (color_green))
				screen.blit(w6_apaches, (hcenter3h - w6_apaches.get_width()/2, vcenter + 190 - w6_apaches.get_height()/2))
			else:
				print "http6 status: ", http6.status
				w6_apaches = xl_font.render(konu_fail, 1, (color_red))
				screen.blit(w6_apaches, (hcenter3h - w6_apaches.get_width()/2, vcenter + 185 - w6_apaches.get_height()/2))
				w6_err = small_font.render("status: " + str(http6.status), 1, (color_red))
				screen.blit(w6_err, (hcenter3h - w6_err.get_width()/2, vcenter + 215 - w6_err.get_height()/2))
		else:
			print "http6 error: ", http6.error
			w6_apaches = xl_font.render(konu_fail, 1, (color_red))
			screen.blit(w6_apaches, (hcenter3h - w6_apaches.get_width()/2, vcenter + 185 - w6_apaches.get_height()/2))
			w6_err = small_font.render("error: " + str(http6.status), 1, (color_red))
			screen.blit(w6_err, (hcenter3h - w6_err.get_width()/2, vcenter + 215 - w6_err.get_height()/2))
		
		#print "End window 6"
		
		#print checkArray("debug", tcp6.result, kon6_limit)
		#print "tcp6 array: " + str(tcp6.result)
		
		#print "Flipping"
		
		#for i in range(1, 13):
		#	screen.blit(div_map, (quarterw*i, 0))
		
		
		#Finish
		pygame.display.flip()
		
		#print "Flipped"

if __name__ == '__main__': main()
