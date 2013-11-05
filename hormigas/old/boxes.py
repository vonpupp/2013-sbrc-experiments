import pygame, pickle, random

class Box:

	def __init__(self, size, id = None):
		self.surface = pygame.Surface(size)
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.surface.fill(self.color)
		self.rect = self.surface.get_rect()
		self.rect.top = 0 - self.rect.height
		self.id = id

# Maybe exists a better way to create a copy of an instance?
def copy(mybox):
	box = Box((mybox.rect.width, mybox.rect.height))
	box.color = mybox.color
	box.surface.fill(box.color)
	box.rect = pygame.Rect(mybox.rect)
	return box

def random_boxes(quantity, minsize, maxsize):
	boxes = []
	id = 0
	for box in range(quantity):
		boxes.append(Box((random.randint(minsize,maxsize),random.randint(minsize,maxsize)),id))
		id += 1
	return boxes

def save_boxes(boxes, file):
	for box in boxes:
		box.surface = None
	save_data(file, boxes)
	for box in boxes:
		box.surface = pygame.Surface((box.rect.width,box.rect.height))
		box.surface.fill(box.color)

def load_boxes(file):
	boxes = load_data(file)
	for box in boxes:
		box.surface = pygame.Surface((box.rect.width,box.rect.height))
		box.surface.fill(box.color)
	return boxes

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

def help():
	print "class Box:	def __init__(self, size, id = None):"
	print "def copy(mybox):return box"
	print "def random_boxes(quantity, minsize, maxsize):return boxes"
	print "def save_boxes(boxes, file):"
	print "def load_boxes(file):return boxes"
	print "def save_data(file, data):return True"
	print "def load_data(file):return data"
