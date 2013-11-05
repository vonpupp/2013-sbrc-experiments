#!/usr/bin/env python

import pygame, time, pickle
import brmodule

class Game:
	
	screen = None
	background = None

	def __init__(self, boxes, container):
		
		self.free_boxes = boxes #COPY!!!
		self.solution = []
		self.container = container

	def update(self):
		
		if self.free_boxes == []:
			return False
		box = self.free_boxes[0]
		if len(self.free_boxes) > 1:
			self.free_boxes = self.free_boxes[1:]
		else:
			self.free_boxes = []
	
		packed = brmodule.pack(box,self.solution,self.container)
		
		if packed:
			return True
		return False

def show_stats(boxes, container):
	total_area = 0
	num_boxes = 0
	min_top = container[1]
	for box in boxes:
		if box.rect.top < min_top:
			min_top = box.rect.top
		total_area += box.rect.height * box.rect.width
		num_boxes += 1
	container_area = container[0]*(container[1] - min_top)
	used_space = float(total_area)/float(container_area) #!
	print 'Used Space: ',total_area
	print '(',used_space * 100.0,'% of ',container_area,' points)'
	print 'Allocated Boxes: ',num_boxes
	return total_area
	
def show(boxes,container):
	screen = pygame.display.set_mode(container)
	for box in boxes:
		if box.rect.top >= 0 and box.rect.left >= 0:
			box.draw(screen)
	end = False
	while not end:
		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == 12:
				end = True
				pygame.display.quit()
		time.sleep(1)
	
def save_data(file, data):
	file_handler = open(file,"wb")
	pickle.dump(data,file_handler)
	file_handler.close()
	return True

def load_data(file):
	file_handler = open(file,"rb")
	data = pickle.load(file_handler)
	file_handler.close()
	return data

#REWRITE USING BOXMODULE AND WITHOUT THE GAME CLASS
def pack(boxes,container): 

	if type(boxes) == type('str'):
		boxes = load_data(boxes)
		for box in boxes:
			box.surface = pygame.Surface((box.rect.width,box.rect.height))
			box.surface.fill(box.color)

	game = Game(boxes,container)
	
	go = True
	while go:
		go = game.update()

	return game.solution
