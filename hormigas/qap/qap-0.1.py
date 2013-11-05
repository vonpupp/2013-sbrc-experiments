#!/usr/bin/env python

import pygame, random, os, sys, matrix, getopt, math

N = 7
TILESIZE = 8
SPEED = 8
ALPHA = 5
BETA = 1
GAMMA = 0.0
ANT_NUMBER = 1

class LinkMatrix:

	'''In the linkmatrix rows will be related to the elements of B, 
	while the columns will be related to the elements of A, the value on 
	each cell of the linkmatrix represents the amount of pheromone present. 
	The linkmatrix represents all the possibilities for connecting A and B'''

	'''Could be nice to work a bit if I can inherit from the matrix class
	instead of adding it as a variable'''

	def __init__(self):
		self.matrix = matrix.Matrix(N**2)

	def draw(self):
		game.screen.lock()
		for i in range(N**2):
			for j in range(N**2):
				color = [0,0,0]
				position = [TILESIZE*(i+2),TILESIZE*(j+2)]
				#pygame.draw.circle(game.screen, [255,255,255], position, 4, 0)
				pygame.draw.circle(game.screen, color, position, 2, 0)
		game.screen.unlock()

	def draw_links(self):
		game.screen.lock()
		for i in range(N**2):
			for j in range(N**2):
				if i < N**2-1:
					for k in range(N**2):
						pheromone_start = self.matrix.__getitem__([i,j])
						pheromone_end = self.matrix.__getitem__([i+1,k])
						if pheromone_start > 0.0 and pheromone_end > 0.0:
							color = [255*(1-pheromone_end),255*(1-pheromone_end),255]
							#color = [0,0,255]
							start = [TILESIZE*(i+2),TILESIZE*(j+2)]
							end = [TILESIZE*(i+3),TILESIZE*(k+2)]
							thickness = 2 # Will be proportional to the cost of the link
							pygame.draw.line(game.screen,color,start,end,thickness)
		game.screen.unlock()

	def pheromone_path(self, path, pheromone):
		x = 0
		for y in path:
			previous = self.matrix.__getitem__([x,y])
			self.matrix.__setitem__([x,y],math.sin(((previous + pheromone)*math.pi)/4))
			x += 1

	def update(self):
		for i in range(N**2):
			for j in range(N**2):
				pheromone = self.matrix.__getitem__([i,j])
				self.matrix.__setitem__([i,j], pheromone*GAMMA)
		
class QAPMatrix:

	'''These will be the problem matrixes, nothing special about them, 
	randomly generated'''

	def __init__(self):
		self.matrix = matrix.Matrix(N)
		for i in range(N):
			for j in range(N):
				self.matrix.__setitem__([i,j], random.random())

	def draw(self):
		print self.matrix

	def update(self):
		pass

class Ant:
	
	def __init__(self):

		self.position = [-1,-1]

		self.center = [0,0]
		self.moves = 0
		self.path = []
		self.path_cost = 0
		self.visited = []
		for node in range(N**2):
			self.visited.append(False) 
	
	def draw(self):
		color = [255,0,0]
		pygame.draw.circle(game.screen, color, self.center, 2, 0)

	def choose_next(self):
		decision = random.random()
		for next in range(N**2):
			decision = decision - game.decisionmatrix.__getitem__([next,self.position[0]])
			if decision < 0.0:
				return next

	def move(self):
		self.center[0] += SPEED
		vspeed = ((self.position[1]+2)*TILESIZE - self.center[1])/self.moves
		self.center[1] += vspeed

	def update(self):
		if not self.moves:
			if self.position[0] > 0:
				[aposx,aposy] = convert(self.position[0])
				[bposx,bposy] = convert(self.position[1])
				self.path_cost += game.amatrix.matrix.__getitem__([aposx,aposy])*game.bmatrix.matrix.__getitem__([bposx,bposy])
			if self.position[0] == N**2-1:
				#print self.path, 1.0/self.path_cost
				game.add_solution(self.path_cost,self.path)
				game.linkmatrix.pheromone_path(self.path,8.0/self.path_cost)
				self.position = [-1,-1]
				self.path = []
				self.path_cost = 0
				self.visited = []
				for node in range(N**2):
					self.visited.append(False) 
			
			'''Next two lines are for repositioning correctly the
			ant after each move'''
			self.center[0] = (self.position[0]+2)*TILESIZE
			self.center[1] = (self.position[1]+2)*TILESIZE
			
			next = self.choose_next()
			self.path.append(next)
			self.visited[next] = True
			
			self.position[0] += 1
			self.position[1] = next
			self.moves = TILESIZE/SPEED
			self.move()
			self.moves -= 1
		else:
			self.move()
			self.moves -= 1
		return True
			

class Game:

	screen = None
	linkmatrix = None
	decisionmatrix = None
	amatrix = None
	bmatrix = None
	ants = None
	iterations = None
	steps = None
	solutions = []

	def __init__(self):
		random.seed()
		pygame.init()

		self.screen = pygame.display.set_mode([(N**2+2)*TILESIZE,(N**2+2)*TILESIZE])
		self.linkmatrix = LinkMatrix()

		self.amatrix = QAPMatrix()
		self.bmatrix = QAPMatrix()

		self.ants = []
		for ant in range(ANT_NUMBER):
			self.ants.append(Ant())
		pygame.display.set_caption("Ant-QAP")
		
		self.iterations = 0
		self.steps = 0

		self.decisionmatrix = self.calc_costmatrix()
	
	def add_solution(self,cost,path):
		for [cost2,path2] in self.solutions:
			if cost == cost2:
				return False
		self.solutions.append([cost,path])
		return True

	def best_solution(self):
		mincost = N**2 # Need to find something like MAXINT
		minpath = []
		for [cost,path] in self.solutions:
			if cost < mincost:
				mincost = cost
				minpath = path
		return [mincost,minpath]
	
	def control(self):
		for e in pygame.event.get():
			if e.type == 12:
				return True
		return False

	def calc_costmatrix(self):
		costmatrix = matrix.Matrix(N**2)
		for i in range(N**2):
			[ax,ay] = convert(i)
			''' There is an enormous possibility of confussion when accesing
			a matrix in terms of 2D position or in row,col position, since the
			coordenates get interchanged between the two'''
			a = self.amatrix.matrix.__getitem__([ay,ax],)
			for j in range(N**2):
				[bx,by] = convert(j)
				b = self.bmatrix.matrix.__getitem__([by,bx],)
				costmatrix.__setitem__([i,j], a*b)
		costmatrix = normalize_columns(costmatrix)
		return costmatrix

	def update(self):

		if self.iterations%(N**2) == 0:
			self.linkmatrix.update()
		if self.iterations%(N**2) == 1:
			cost, path = self.best_solution()
			print cost, len(self.solutions)
			self.solutions = []
			self.screen.fill((255,255,255))
			self.linkmatrix.draw_links()
			pheromonematrix = normalize_columns(self.linkmatrix.matrix)
			costmatrix = self.calc_costmatrix()
			pheromonematrix = power_matrix(pheromonematrix,BETA)
			costmatrix = power_matrix(costmatrix,ALPHA)
			#pheromonematrix = multiply_escalar(pheromonematrix,BETA)
			#costmatrix = multiply_escalar(costmatrix,ALPHA)
			self.decisionmatrix = multiply_cartesian(pheromonematrix,costmatrix)
			self.decisionmatrix = normalize_columns(self.decisionmatrix)
		self.linkmatrix.draw()

		'''Next line is a dirty hack, is not very logical to calculate a
		N**2 vector of probabilities for each ant when each of them is going
		to use exactly the same, so we calculate it for the first ant and
		store it on game.decision_vector, could be more logical to do the
		entire decision matrix when drawing the links, but it's harder...'''
		#self.decision_vector = calculate_decision_vector(self.ants[0].position[0])
		for ant in self.ants:
			ant.update()
			ant.draw()
		
		pygame.display.flip()
		
		self.iterations += 1

		return True

def convert(position):
	posx = position%N
	posy = position/N
	return [posx,posy]

def power_matrix(matrix, factor):
	rows = matrix.rows()
	cols = matrix.cols()
	for i in range(rows):
		for j in range(cols):
			base = matrix.__getitem__([i,j])
			matrix.__setitem__([i,j], base**factor)
	return matrix

def multiply_cartesian(amatrix,bmatrix):
	'''I'm not going to prevent bad use of this function, as is for private
	use and I know what to not do'''
	rows = amatrix.rows()
	cols = amatrix.cols()
	cmatrix = matrix.Matrix(rows,cols)
	for i in range(rows):
		for j in range(cols):
			a = amatrix.__getitem__([i,j])
			b = amatrix.__getitem__([i,j])
			cmatrix.__setitem__([i,j],a*b)
	return cmatrix
	
def multiply_escalar(matrix,escalar):
	'''I'm not going to prevent bad use of this function, as is for private
	use and I know what to not do'''
	rows = matrix.rows()
	cols = matrix.cols()
	for i in range(rows):
		for j in range(cols):
			a = matrix.__getitem__([i,j])
			matrix.__setitem__([i,j],a*escalar)
	return matrix
	

def normalize_columns(m):
	rows = m.rows()
	cols = m.cols()
	normalized = matrix.Matrix(rows,cols)
	for j in range(cols):
		total = 0.0
		for i in range(rows):
			total += m.__getitem__([i,j])
		if total > 0.0:
			for i in range(rows):
				normalized.__setitem__([i,j],m.__getitem__([i,j])/total)
		else:
			for i in range(rows):
				normalized.__setitem__([i,j],1.0/rows)
	return normalized

def normalize(vector):
	total = 0
	for x in vector:
		total += x
	if total != 0:
		for position in range(len(vector)):
			vector[position] = vector[position]/total
	return vector
				
def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

def usage():
	print "Usage Instructions"

def main():
	
	global VERBOSE
	VERBOSE = False
	
	try:
		opts,args = getopt.getopt(sys.argv[1:],"hv", ["help","verbose"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt,arg in opts:
		if opt in ("-v","--verbose"):
			VERBOSE = True
		if opt in ("-h","-help"):
			usage()
			sys.exit()

	global game
	game = Game()
	
	done = False
	while not done:
		game.update()
		done = game.control()

if __name__ == "__main__":
	main()
