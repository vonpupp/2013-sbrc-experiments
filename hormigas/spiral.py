import matrix

class BoxSpiral:
	
	def __init__(self, boxes):
		x = 0
		for box in boxes:
			x = max(box.id,x)
		#self.correspondences = matrix.Matrix(x)
		self.nextpoint = (0,0)
		self.direction = 'up'
		self.openbox = None #Deberia ser el cardinal de openbox en self.solution
		self.lastbox = None #Es la longitud de self.solution - 1
		self.solution = []

	def outside(self):
		if self.direction == 'up':
			return 'left'
		if self.direction == 'right':
			return 'up'
		if self.direction == 'down':
			return 'right'
		if self.direction == 'left':
			return 'down'
		return False

	def inside(self):
		if self.direction == 'up':
			return 'right'
		if self.direction == 'right':
			return 'down'
		if self.direction == 'down':
			return 'left'
		if self.direction == 'left':
			return 'up'
		return False

	def forward(self):
		return self.direction

	def backward(self):
		if self.direction == 'up':
			return 'down'
		if self.direction == 'right':
			return 'left'
		if self.direction == 'down':
			return 'up'
		if self.direction == 'left':
			return 'right'
		return False

	def nextpoint(self,newbox):
		openbox = self.solution[self.openbox]
		# Determine the next point to put a box
		# newbox is the last packed box
		if self.direction == 'up':
			x = newbox.rect.right
			y = newbox.rect.top
			if newbox.rect.top == openbox.rect.bottom:
				x = max(newbox.rect.left,openbox.rect.left)
			self.nextpoint = (x,y)
			return True
		if self.direction == 'right':
			x = newbox.rect.right
			y = newbox.rect.bottom
			if newbox.rect.right == openbox.rect.left:
				y = max(newbox.rect.top,openbox.rect.top)
			self.nextpoint = (x,y)
			return True
		if self.direction == 'down':
			x = newbox.rect.left
			y = newbox.rect.bottom
			if newbox.rect.bottom == openbox.rect.top:
				x = min(newbox.rect.right,openbox.rect.right)
			self.nextpoint = (x,y)
			return True
		if self.direction == 'left':
			x = newbox.rect.left
			y = newbox.rect.top
			if newbox.rect.left == openbox.rect.right:
				y = min(newbox.rect.bottom,openbox.rect.bottom)
			self.nextpoint = (x,y)
			return True
		return False
	
	def pack(self,box):
		# Put in self.nextpoint
		if self.direction == 'up':
			box.rect.left = self.nextpoint[0] + box.width
			box.rect.top = self.nextpoint[1] + box.height
		if self.direction == 'right':
			box.rect.left = self.nextpoint[0]
			box.rect.top = self.nextpoint[1] + box.height
		if self.direction == 'down':
			box.rect.left = self.nextpoint[0]
			box.rect.top = self.nextpoint[1]
		if self.direction == 'left':
			box.rect.left = self.nextpoint[0] + box.width
			box.rect.top = self.nextpoint[1]
		
		# Check collisions with self.openbox and the N followers
		lastbox = self.solution[len(self.solution)-1]
		for i in range(self.openbox,len(self.solution)):
			openbox = self.solution[self.openbox]
			if box.collide(self.solution[i]):
				# If anyone collides becomes self.openbox
				self.openbox = i
				#	slide to the outside
				box.put_out(openbox,self.outside())
				#	slide backwards
				if not box.touch(lastbox):
					box.put_out(lastbox,self.outside())
					box.put_out(openbox,self.backward())
					previousbox = self.solution[len(self.solution)-2]
					# If it collides again with the previous box to lastbox...
					# (Check length of lastbox and box)
					if box.collide(previousbox):
						box.put_out(previousbox,self.outside())
		
		# Slide to the inside (No effect if there was a collision)
		# (Check the borders of the N previous of openbox to find which ones could collide)
		# Change direction
		# Actualize self.correspondences
		# Get new self.nextpoint
		pass

