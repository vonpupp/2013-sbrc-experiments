#!/usr/bin/env python

import pygame, random, os, sys, getopt, pickle, types

class Box:

	def __init__(self, size = None):
		if size == None:
			size = 	(random.randint(BOXSIZE[0],BOXSIZE[1]),random.randint(BOXSIZE[0],BOXSIZE[1]))
		self.surface = pygame.Surface(size)
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.surface.fill(self.color)
		self.rect = self.surface.get_rect()

class Game:
	
	screen = None
	background = None

	def __init__(self, boxes = None):
		
		self.free_boxes = []
		self.solution = []

		if VISUAL:
			self.screen = pygame.display.set_mode((WINSIZE[0]+(BOXSIZE[1]+BOXSIZE[0]*2),WINSIZE[1]))
			pygame.display.set_caption("pack")
			self.background = pygame.Surface((WINSIZE[0]+(BOXSIZE[1]+BOXSIZE[0]*2),WINSIZE[1]))
			self.background.fill((200,200,200))
			tmp = pygame.Surface(WINSIZE)
			tmp.fill((255,255,255))
			self.background.blit(tmp,(0,0))
		
		if boxes != None:
			self.free_boxes = boxes
		else:
			if LOAD_BOXES != None:
				self.load_boxes()
			else:
				self.new_free_boxes(BOXES)
		
		if SAVE_BOXES != None:
			self.save_boxes()	

	def save_boxes(self):
		for box in self.free_boxes:
			box.surface = None
		save_data(SAVE_BOXES, self.free_boxes)
		for box in self.free_boxes:
			box.surface = pygame.Surface((box.rect.width,box.rect.height))
			box.surface.fill(box.color)

	def load_boxes(self):
		self.free_boxes = load_data(LOAD_BOXES)
		for box in self.free_boxes:
			box.surface = pygame.Surface((box.rect.width,box.rect.height))
			box.surface.fill(box.color)

	def control(self):
		for e in pygame.event.get():
			if e.type == 12:
				return True
		return False

	def new_free_boxes(self,number):
		for i in range(number):
			self.free_boxes.append(Box())

	def draw_free_boxes(self):
		top = BOXSIZE[1]
		for box in self.free_boxes:
			self.screen.blit(box.surface,(WINSIZE[0]+BOXSIZE[0],top))
			top += BOXSIZE[1]*2

	def find_box_at(x,y):
		for [box,position] in solution:
			rect = box.get_rect()
			rect.top = position[0]
			rect.left = position[1]
			if x > rect.left and x < rect.right and y > rect.top and y < rect.bottom: 
				return box
		return False

	def collide_down(self,mybox):
		collidebox = None
		collidetop = WINSIZE[1]
		for box in self.solution:
			if box.rect.top >= mybox.rect.bottom:
				if mybox.rect.left <= box.rect.left and mybox.rect.right >= box.rect.right:
					if box.rect.top < collidetop:
						collidetop = box.rect.top
						collidebox = box
				if mybox.rect.right <= box.rect.right and mybox.rect.left >= box.rect.left:
					if box.rect.top < collidetop:
						collidetop = box.rect.top
						collidebox = box
				if mybox.rect.left < box.rect.left and mybox.rect.right > box.rect.left:
					if box.rect.top < collidetop:
						collidetop = box.rect.top
						collidebox = box
				if mybox.rect.left < box.rect.right and mybox.rect.right > box.rect.right:
					if box.rect.top < collidetop:
						collidetop = box.rect.top
						collidebox = box
		return collidebox

	def collide_right(self,mybox):
		collidebox = None
		collideleft = WINSIZE[0]
		for box in self.solution:
			if box.rect.left >= mybox.rect.right:
				if mybox.rect.top <= box.rect.top and mybox.rect.bottom >= box.rect.bottom:
					if box.rect.left < collideleft:
						collideleft = box.rect.left
						collidebox = box
				if mybox.rect.bottom <= box.rect.bottom and mybox.rect.top >= box.rect.top:
					if box.rect.left < collideleft:
						collideleft = box.rect.left
						collidebox = box
				if mybox.rect.top < box.rect.top and mybox.rect.bottom > box.rect.top:
					if box.rect.left < collideleft:
						collideleft = box.rect.left
						collidebox = box
				if mybox.rect.top < box.rect.bottom and mybox.rect.bottom > box.rect.bottom:
					if box.rect.left < collideleft:
						collideleft = box.rect.left
						collidebox = box
		return collidebox
		
	def slide_right(self,mybox,slidebox = None):
		collidebox = self.collide_right(mybox)
		if slidebox == None:
			if collidebox != None:
				mybox.rect.left = collidebox.rect.left - mybox.rect.width
			else:
				mybox.rect.left = WINSIZE[0] - mybox.rect.width
			return False
		else:
			if collidebox == None:
				if slidebox.rect.right + mybox.rect.width < WINSIZE[0]:
					mybox.rect.left = slidebox.rect.right
					return True
				else:
					mybox.rect.left = WINSIZE[0] - mybox.rect.width
					return False
			else:
				if collidebox.rect.left < slidebox.rect.right + mybox.rect.width:
					mybox.rect.left = collidebox.rect.left - mybox.rect.width
					return False
				else:
					mybox.rect.left = slidebox.rect.right
					return True
		return False

	def pack(self,mybox):
		mybox.rect.top = 0 - mybox.rect.height
		
		while True:
			collidebox = self.collide_down(mybox)
			if collidebox != None:
				mybox.rect.top = collidebox.rect.top - mybox.rect.height
			else:
				mybox.rect.top = WINSIZE[1] - mybox.rect.height
			
			free = self.slide_right(mybox,collidebox)
			
			if not free:
				break
			
		if mybox.rect.top < 0:
			return False
		self.solution.append(mybox)
		return True
	
	def draw_solution(self):
		for box in self.solution:
			self.screen.blit(box.surface, box.rect)

	def show_stats(self):
		total_area = 0
		num_boxes = 0
		min_top = WINSIZE[1]
		for box in self.solution:
			if box.rect.top < min_top:
				min_top = box.rect.top
			total_area += box.rect.height * box.rect.width
			num_boxes += 1
		container_area = WINSIZE[0]*(WINSIZE[1] - min_top)
		used_space = float(total_area)/float(container_area)
		print 'Used Space: ',used_space * 100.0,'%'
		print '\tof: ',container_area,' points'
		print 'Allocated Boxes: ',num_boxes
	
	def update(self):
		
		if self.free_boxes == []:
			return False
		box = self.free_boxes[0]
		if len(self.free_boxes) > 1:
			self.free_boxes = self.free_boxes[1:]
		else:
			self.free_boxes = []
	
		packed = self.pack(box)
		
		if packed:
			if VISUAL:
				self.screen.blit(self.background,(0,0))
				self.draw_solution()
				self.draw_free_boxes()
				pygame.display.flip()
			return True
		return False

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

def get_game_options():
	
	global FPS
	FPS = 25
	global LOAD_BOXES, SAVE_BOXES
	LOAD_BOXES = None
	SAVE_BOXES = None
	global BOXES
	BOXES = 100
	global VISUAL
	VISUAL = False
	global WINSIZE
	WINSIZE = [512,512]
	global BOXSIZE
	BOXSIZE = [16,64]

	try:
		opts,args = getopt.getopt(sys.argv[1:],"hVl:s:f:b:H:W:m:M:",["help","Visual","load=","save=","fps=","boxes=","Height=","Width=","minbox=","Maxbox="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt,arg in opts:
		if opt in ("-h","--help"):
			usage()
			sys.exit()
		if opt in ("-V","--Visual"):
			VISUAL = True
		if opt in ("-l","--load"):
			LOAD_BOXES = arg
		if opt in ("-s","--save"):
			SAVE_BOXES = arg
		if opt in ("-b","--boxes"):
			BOXES = int(arg)
		if opt in ("-f","--fps"):
			FPS = int(arg)
		if opt in ("-W","--Width"):
			WINSIZE[0] = int(arg)
		if opt in ("-H","--Height"):
			WINSIZE[1] = int(arg)
		if opt in ("-m","--minbox"):
			BOXSIZE[0] = int(arg)
		if opt in ("-M","--Maxbox"):
			BOXSIZE[1] = int(arg)

def usage():
	print "         Usage Instructions"
	print ""
	print "     -h: Shows this help (--help)"
	print ""
	print "     -V: Show packing graphically (--Visual)"
	print ""
	print "-l file: Loads a group of boxes from file,"
	print "         ignores the --boxes option (--load=file)"
	print ""
	print "-s file: Saves the boxes generated to file (--save=file)"
	print ""
	print " -b int: Generates int boxes (--boxes=int)"
	print ""
	print " -f int: Runs at int fps as maximum (--fps=int)"
	print ""
	print " -W int: Sets the width of the container to int (--Width=int)"
	print ""
	print " -H int: Sets the height of the container to int (--Height=int)"
	print ""
	print " -m int: Sets the minimum side size of the boxes to int (--minbox=int)"
	print ""
	print " -M int: Sets the maximum side size of the boxes to int (--Maxbox=int)"

def init():
	
	import pygame, random, os, sys, getopt, pickle, types
	
	random.seed()
	pygame.init()
	get_game_options()

def pack(boxes):

	if type(boxes) == type('str'):
		boxes = load_data(boxes)
		for box in boxes:
			box.surface = pygame.Surface((box.rect.width,box.rect.height))
			box.surface.fill(box.color)

	game = Game(boxes)
	
	go = True
	while go:
		go = game.update()
	game.show_stats()

def main():

	random.seed()
	pygame.init()

	get_game_options()

	game = Game()

	clock = pygame.time.Clock()

	quit = False
	go = True
	show_stats = True
	while not quit:
		clock.tick(FPS)
		if go:
			go = game.update()
		else:
			if show_stats:
				show_stats = False
				game.show_stats()
				if not VISUAL:
					break
		quit = game.control()

if __name__ == "__main__":
	main()
