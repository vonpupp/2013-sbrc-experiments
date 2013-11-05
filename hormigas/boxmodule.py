import pygame, pickle, random

class Box:

	def __init__(self, size, id):
		self.surface = pygame.Surface(size)
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.surface.fill(self.color)
		self.rect = self.surface.get_rect()
		self.rect.top = 0 - self.rect.height
		self.id = id

	def draw(self,surface):
		#pygame.font.init()
		#font = pygame.font.Font(None,16)
		#n = font.render(str(self.id),True,(0,0,0))
		#self.surface.blit(n,n.get_rect())
		surface.blit(self.surface, self.rect)
		

	def inside(self,point):
		x = point[0]
		y = point[1]
		if self.rect.left <= x and x < self.rect.right \
		and self.rect.top <= y and y < self.rect.bottom:
			return True
		return False

	def copy(self):
		box = Box((self.rect.width, self.rect.height),self.id)
		box.color = self.color
		box.surface.fill(box.color)
		box.rect = pygame.Rect(self.rect)
		return box

	def collide(self,box):
		for point in (self.rect.topleft),\
			((self.rect.top, self.rect.right-1)),\
			((self.rect.bottom-1, self.rect.left)),\
			((self.rect.bottom-1, self.rect.right-1)):
			if box.inside(point):
				return True
		for point in (box.rect.topleft),\
			((box.rect.top, box.rect.right-1)),\
			((box.rect.bottom-1, box.rect.left)),\
			((box.rect.bottom-1, box.rect.right-1)):
			if self.inside(point):
				return True
		return False

	def touch(self,box):
		if not self.collide(box):
			if self.rect.top == box.rect.bottom:
				if self.rect.left <= box.rect.left and self.rect.right > box.rect.left:
					return True
				if self.rect.left < box.rect.right and self.rect.right >= box.rect.right:
					return True
				if self.rect.left <= box.rect.left and self.rect.right >= box.rect.right:
					return True
				if self.rect.left >= box.rect.left and self.rect.right <= box.rect.right:
					return True
			if self.rect.bottom == box.rect.top:
				if self.rect.left <= box.rect.left and self.rect.right > box.rect.left:
					return True
				if self.rect.left < box.rect.right and self.rect.right >= box.rect.right:
					return True
				if self.rect.left <= box.rect.left and self.rect.right >= box.rect.right:
					return True
				if self.rect.left >= box.rect.left and self.rect.right <= box.rect.right:
					return True
			if self.rect.left == box.rect.right:
				if self.rect.top <= box.rect.top and self.rect.bottom > box.rect.top:
					return True
				if self.rect.top < box.rect.bottom and self.rect.bottom >= box.rect.bottom:
					return True
				if self.rect.top <= box.rect.top and self.rect.bottom >= box.rect.bottom:
					return True
				if self.rect.top >= box.rect.top and self.rect.bottom <= box.rect.bottom:
					return True
			if self.rect.right == box.rect.left:
				if self.rect.top <= box.rect.top and self.rect.bottom > box.rect.top:
					return True
				if self.rect.top < box.rect.bottom and self.rect.bottom >= box.rect.bottom:
					return True
				if self.rect.top <= box.rect.top and self.rect.bottom >= box.rect.bottom:
					return True
				if self.rect.top >= box.rect.top and self.rect.bottom <= box.rect.bottom:
					return True
		return False

	def put_out(self,box,direction):
		# Aligns self outside with the box in the named direction
		if direction == 'up':
			self.rect.top = box.rect.top - self.rect.height
		if direction == 'right':
			self.rect.left = box.rect.right
		if direction == 'down':
			self.rect.top = box.rect.bottom
		if direction == 'left':
			self.rect.left = box.rect.left - self.rect.width
		
	def put_in(self,box,direction):
		# Aligns self inside with the box in the named direction 
		if direction == 'up':
			self.rect.top = box.rect.top
		if direction == 'right':
			self.rect.left = box.rect.right - self.rect.width
		if direction == 'down':
			self.rect.top = box.rect.bottom - self.rect.height
		if direction == 'left':
			self.rect.left = box.rect.left
		
def random_boxes(quantity, minsize, maxsize):
	boxes = []
	id = 0
	for box in range(quantity):
		boxes.append(Box((random.randint(minsize,maxsize),random.randint(minsize,maxsize)),id))
		id += 1
	return boxes

def pp_boxes(container,maxsize):
	boxes = [Box(container,0)]
	done = False
	while not done:
		done = True
		newboxes = []
		for box in boxes:
			moreboxes = divide_box(box,maxsize)
			if len(moreboxes) != 1:
				done = False
			for mb in moreboxes:
				newboxes.append(mb)
		boxes = []
		i = 0
		for box in newboxes:
			box.id = i
			i += 1
			boxes.append(box)
	return boxes
				
				
def divide_box(box,maxsize):
	boxes = []
	if box.rect.height > maxsize:
		box1 = Box((box.rect.width,box.rect.height/random.randint(2,4)),box.id)
		box2 = Box((box.rect.width,box.rect.height/random.randint(2,4)),box.id)
		if box1.rect.height + box2.rect.height < box.rect.height:
			box1.rect.height += 1
		todivide = [box1,box2]
	else:
		todivide = [box]
	for box in todivide:
		if box.rect.width > maxsize:
			box1 = Box((box.rect.width/random.randint(2,4),box.rect.height),box.id)
			box2 = Box((box.rect.width/random.randint(2,4),box.rect.height),box.id)
			if box1.rect.width + box2.rect.width < box.rect.width:
				box1.rect.height += 1
			boxes.append(box1)
			boxes.append(box2)
		else:
			boxes.append(box)
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
