#!/usr/bin/python

import pygame

pygame.init()
pygame.display.set_mode([128,128])
done = False
while not done:
	for e in pygame.event.get():
		if e.type == 12:
			done = True
		if e.type == 3:
			print e.key
		if e.type == 6:
			print e.button,e.pos
