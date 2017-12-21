#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Main test (Emvivre)

Inspired from Empty Laser (Sam Neurohack) 
LICENCE : CC
'''

import pygame
import math
import random
import itertools
import sys
import os
import thread
import time
import frame
import renderer
import dac
from globalVars import *

import gstt

def dac_thread():
	while True:
		try:
			d = dac.DAC(dac.find_first_dac())
			d.play_stream(laser)
		except Exception as e:

			import sys, traceback
			print '\n---------------------'
			print 'Exception: %s' % e
			print '- - - - - - - - - - -'
			traceback.print_tb(sys.exc_info()[2])
			print "\n"
			pass

def DrawTestPattern(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF)
	f.LineTo((l, h), 0xFFFFFF)
	f.LineTo((0, h), 0xFFFFFF)
	f.LineTo((0, 0), 0xFFFFFF)
	
	f.LineTo((2*L_SLOPE, h), 0)
	for i in xrange(1,7):
		c = (0xFF0000 if i & 1 else 0) | (0xFF00 if i & 2 else 0) | (0xFF if i & 4 else 0)
		f.LineTo(((2 * i + 1) * L_SLOPE, 0), c)
		f.LineTo(((2 * i + 2) * L_SLOPE, h), c)
	f.Line((l*.5, h*.5), (l*.75, -h*.5), 0xFF00FF)
	f.LineTo((l*1.5, h*.5), 0xFF00FF)
	f.LineTo((l*.75, h*1.5), 0xFF00FF)
	f.LineTo((l*.5, h*.5), 0xFF00FF)

def Align(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF)
	f.LineTo((l, h), 0xFFFFFF)
	f.LineTo((0, h), 0xFFFFFF)
	f.LineTo((0, 0), 0xFFFFFF)
	laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

	print str(gstt.centerx) + "," + str(gstt.centery) + "," + str(gstt.zoomx) + "," + str(gstt.zoomy) + "," + str(gstt.sizex) + "," + str(gstt.sizey)


app_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Empty Laser")
clock = pygame.time.Clock()

gstt.centerx = LASER_CENTER_X
gstt.centery = LASER_CENTER_Y
gstt.zoomx = LASER_ZOOM_X
gstt.zoomy = LASER_ZOOM_Y
gstt.sizex = LASER_SIZE_X
gstt.sizey = LASER_SIZE_Y
gstt.finangle = LASER_ANGLE

fwork_holder = frame.FrameHolder()
laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)
thread.start_new_thread(dac_thread, ())

update_screen = False
keystates = pygame.key.get_pressed()

(SCREEN_W, SCREEN_H) = screen_size

def draw_circle():
        dots = []
        
        PI = math.pi
        amp = 200
        nb_point = 12
        for t in range(0, nb_point+1):
                y = (SCREEN_H/2) - amp*math.sin(2*PI*(float(t)/float(nb_point)))
                x = (SCREEN_W/2) - amp*math.cos(2*PI*(float(t)/float(nb_point)))
                dots.append((int(x),int(y)))
        return dots

def draw_hour(p):
        amp=100
        PI=math.pi
        x = (SCREEN_W/2) - amp*math.cos(2*PI*(p/12.))
        y = (SCREEN_H/2) - amp*math.sin(2*PI*(p/12.))
        dots = [(SCREEN_W/2, SCREEN_H/2), (x, y)]
        return dots

def draw_minute(p):
        amp=180
        PI=math.pi
        x = (SCREEN_W/2) - amp*math.cos(2*PI*(p/60.))
        y = (SCREEN_H/2) - amp*math.sin(2*PI*(p/60.))
        dots = [(SCREEN_W/2, SCREEN_H/2), (x, y)]
        return dots

tick = 0
hour_i = 0
minute_i = 0

def draw_sine(f):
        dots = []
        
        PI = math.pi
        amp = 200
        nb_point = 24
        for t in range(0, nb_point+1):
                y = (SCREEN_H/2) - amp*math.sin(2*PI*(float(t)/float(nb_point)))
                x = (SCREEN_W/2) - amp*math.cos(2*PI*f*(float(t)/float(nb_point)))
                dots.append((int(x),int(y)))
        return dots

f_sine = 0

################
def draw_laser_panel(tick):
        dots = []
        PI = math.pi
        amp = 200
        nb_point = 24        
        for t in range(0, nb_point+1):
                if t % 2 == 0:
                        amp = 180 * abs(math.sin((float(tick)/100)))
                else:
                        amp = 120 * abs(math.sin((float(tick)/100)))
                y = (SCREEN_H/2) - amp*math.sin(2*PI*(float(t)/float(nb_point)))
                x = (SCREEN_W/2) - amp*math.cos(2*PI*(float(t)/float(nb_point)))
                dots.append((int(x),int(y)))
                dots.append((int(SCREEN_W/2),int(SCREEN_H/2)))
        return dots

game_state = 0
subtick = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			break

	keystates_prev = keystates[:]
	keystates = pygame.key.get_pressed()[:]

        if keystates[pygame.K_ESCAPE]:
                break

        ###############################
        # THINKING PHASE
        # lines_to_display = [(0,0), (SCREEN_W,0), (SCREEN_W-1, SCREEN_H-1), (0,SCREEN_H-1), (0,0)]
        #n = 3
        #lines_to_display = [(0,0), (SCREEN_W/n,0), (SCREEN_W/n-1, SCREEN_H/n-1), (0,SCREEN_H/n-1), (0,0)]
        
        
        ###############################               	
	screen.fill(0)
	fwork = frame.Frame()
	
	# Alignement Case
	
	if keystates[pygame.K_p]:
		DrawTestPattern(fwork)
		
	if keystates[pygame.K_x]:
		Align(fwork)
		
	if keystates[pygame.K_r]:
		gstt.centerx += 20
		Align(fwork)

	if keystates[pygame.K_t]:
		gstt.centerx -= 20
		Align(fwork)
		
	if keystates[pygame.K_y]:
		gstt.centery += 20
		Align(fwork)

	if keystates[pygame.K_u]:
		gstt.centery -= 20
		Align(fwork)

	if keystates[pygame.K_f]:
		gstt.zoomx += 0.1
		Align(fwork)

	if keystates[pygame.K_g]:
		gstt.zoomx -= 0.1
		Align(fwork)
		
	if keystates[pygame.K_h]:
		gstt.zoomy += 0.1
		Align(fwork)

	if keystates[pygame.K_j]:
		gstt.zoomy -= 0.1
		Align(fwork)
	
	if keystates[pygame.K_c]:
		gstt.sizex -= 50
		Align(fwork)
		
	if keystates[pygame.K_v]:
		gstt.sizex += 50
		Align(fwork)
		
	if keystates[pygame.K_b]:
		gstt.sizey -= 50
		Align(fwork)
		
	if keystates[pygame.K_n]:
		gstt.sizey += 50
		Align(fwork)
		
	if keystates[pygame.K_l]:
		gstt.finangle -= 0.001
		Align(fwork)
		
	if keystates[pygame.K_m]:
		gstt.finangle += 0.001
		Align(fwork)


        ###############################
        # DRAWING PHASE
        tick += 1

        # cloc
        if game_state == 0:
                fwork.PolyLineOneColor(draw_circle(), c=0xFF0000 )
                fwork.PolyLineOneColor(draw_hour(hour_i), c=0xFFFFFF )
                fwork.PolyLineOneColor(draw_minute(minute_i), c=0x00FFFF )
                minute_i += 1
                if tick % 60 == 0:
                        hour_i += 1

                if subtick > 60*5:
                        game_state += 1
                        subtick = 0
                        f_sine = 0
                        
                        
        # lissajou
        if game_state == 1:
                fwork.PolyLineOneColor( draw_sine(f_sine), c=0xFF0000 )
                if f_sine > 24:
                        f_sine = 0
                        game_state += 1
                        subtick = 0
                
                f_sine += 0.01

        if game_state == 2:
                fwork.PolyLineOneColor(draw_laser_panel(tick), c=0x00FF00)
                if subtick == 300:
                        game_state = 0
                        subtick = 0
                
        if game_state == 3:
                pass

        subtick += 1
                
        ###############################               	
                       
	
	fwork_holder.f = fwork

	if update_screen:
		update_screen = False
		fwork.RenderScreen(screen)
		pygame.display.flip()
	else:
		update_screen = True
	clock.tick(100)

pygame.quit()


