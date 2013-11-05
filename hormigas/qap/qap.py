#!/usr/bin/env python

import pygame, random, os, sys, matrix, getopt, math, pickle

N = 5
TILESIZE = 8
ALPHA = 1		# Importance of the cost
BETA = 5		# Importance of the pheromones
GAMMA = 0.0		# Pheromone survival rate
DELTA = 1		# Bad path tolerance
ANT_NUMBER = N**2

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
				cost = game.costmatrix.__getitem__([j,i])*255*(N**2)/2
				if cost > 255:
					cost = 255
				color = [255-cost,255-cost,255-cost]
				position = [TILESIZE*(i+2),TILESIZE*(j+2)]
				pygame.draw.circle(game.screen, color, position, 2, 0)
		game.screen.unlock()

	def draw_links(self):
		game.screen.lock()
		for i in range(N**2):
			for j in range(N**2):
				if i < N**2-1:
					for k in range(N**2):
						pheromone_start = self.matrix.__getitem__([j,i])
						pheromone_end = self.matrix.__getitem__([k,i+1])
						if pheromone_start > 0.0 and pheromone_end > 0.0:
							color = [0,0,255]
							start = [TILESIZE*(i+2),TILESIZE*(j+2)]
							end = [TILESIZE*(i+3),TILESIZE*(k+2)]
							thickness = 2 # Will be proportional to the cost of the link
							pygame.draw.line(game.screen,color,start,end,thickness)
		game.screen.unlock()

	def pheromone_path(self, path, pheromone):
		x = 0
		for y in path:
			previous = self.matrix.__getitem__([y,x])
			self.matrix.__setitem__([y,x],previous + pheromone)
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
			decision = decision - game.decisionmatrix.__getitem__([next,self.position[0]+1])
			if decision < 0.0:
				if not self.visited[next]:
					return next
		return 0

	def update(self):
		
		self.position[0] = game.iteration
		
		'''Next two lines are for repositioning correctly the
		ant after each move'''
		self.center[0] = (self.position[0]+2)*TILESIZE
		self.center[1] = (self.position[1]+2)*TILESIZE
		
		[aposx,aposy] = convert(self.position[0])
		[bposx,bposy] = convert(self.position[1])
		self.path_cost += game.amatrix.matrix.__getitem__([aposx,aposy])*game.bmatrix.matrix.__getitem__([bposx,bposy])
		
		if self.position[0] == N**2-1:
			worstcost = game.worstcost*DELTA
			if self.path_cost <= worstcost:
				game.add_solution(self.path_cost,self.path)
				game.linkmatrix.pheromone_path(self.path,1.0/self.path_cost)
			self.position = [-1,-1]
			self.path = []
			self.path_cost = 0
			self.visited = []
			for node in range(N**2):
				self.visited.append(False) 
			
		next = self.choose_next()
		self.position[1] = next
		self.path.append(next)
		self.visited[next] = True
		
		return True
			
class Game:

	screen = None
	linkmatrix = None
	decisionmatrix = None
	costmatrix = None
	amatrix = None
	bmatrix = None
	ants = None
	iteration = None
	total_iterations = None
	steps = None
	solutions = []
	worstcost = None

	def __init__(self):
		random.seed()
		pygame.init()
		
		if VISUAL:
			self.screen = pygame.display.set_mode([(N**2+2)*TILESIZE,(N**2+2)*TILESIZE])
			pygame.display.set_caption("Ant-QAP")
			self.screen.fill((255,255,255))
		
		self.linkmatrix = LinkMatrix()

		if AMATRIX_LOAD != None:
			self.amatrix = self.load_data(AMATRIX_LOAD)
		else:
			self.amatrix = QAPMatrix()

		if BMATRIX_LOAD != None:
			self.bmatrix = self.load_data(BMATRIX_LOAD)
		else:
			self.bmatrix = QAPMatrix()
		
		if AMATRIX_SAVE != None:
			self.save_data(AMATRIX_SAVE,self.amatrix)

		if BMATRIX_SAVE != None:
			self.save_data(BMATRIX_SAVE,self.bmatrix)

		self.ants = []
		for ant in range(ANT_NUMBER):
			self.ants.append(Ant())
		
		self.total_iterations = 0
		self.iteration = 0
		self.steps = 0

		self.costmatrix = self.calc_costmatrix()
		self.costmatrix = normalize_columns(self.costmatrix)
		self.decisionmatrix = self.costmatrix
	
		self.worstcost = N**2
	
	def save_data(self, file, data):
		file_handler = open(file,"wb")
		pickle.dump(data,file_handler)
		file_handler.close()
		return True
	
	def load_data(self, file):
		file_handler = open(file,"rb")
		data = pickle.load(file_handler)
		file_handler.close()
		return data
	
	def add_solution(self,cost,path):
		'''for [cost2,path2] in self.solutions:
			if cost == cost2:
				return False'''
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
	
	def medium_solution(self):
		totalcost = 0
		for [cost,path] in self.solutions:
			totalcost += cost
		return totalcost/len(self.solutions)
	
	def worst_solution(self):
		maxcost = 0 # Need to find something like MAXINT
		maxpath = []
		for [cost,path] in self.solutions:
			if cost > maxcost:
				maxcost = cost
				maxpath = path
		return [maxcost,maxpath]
	
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
			a = self.amatrix.matrix.__getitem__([ay,ax])
			for j in range(N**2):
				[bx,by] = convert(j)
				b = self.bmatrix.matrix.__getitem__([by,bx])
				costmatrix.__setitem__([j,i], 1-a*b)
		return costmatrix

	def update(self):

		if self.iteration == N**2:
			self.total_iterations += 1
			if self.solutions != []:
				cost, path = self.best_solution()
				self.worstcost, worstpath = self.worst_solution()
				media = self.medium_solution()
				self.solutions = []
				print self.total_iterations, '-', cost,'--', media
				if self.total_iterations == ITERATIONS:
					sys.exit()
				if VISUAL:
					self.screen.fill((255,255,255))
					self.linkmatrix.draw_links()
				self.decisionmatrix = normalize_columns(self.linkmatrix.matrix)
				self.decisionmatrix = multiply_escalar(self.decisionmatrix,BETA)
				self.decisionmatrix = sum_matrix(self.decisionmatrix, self.costmatrix)
				self.decisionmatrix = normalize_columns(self.decisionmatrix)
				self.linkmatrix.update()
			self.iteration = 0
		
		if VISUAL:
			self.linkmatrix.draw()
		
		for ant in self.ants:
			ant.update()
			if VISUAL:
				ant.draw()
		if VISUAL:
			pygame.display.flip()
		
		self.iteration += 1

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

def sum_matrix(amatrix,bmatrix):
	'''I'm not going to prevent bad use of this function, as is for private
	use and I know what to not do'''
	rows = amatrix.rows()
	cols = amatrix.cols()
	cmatrix = matrix.Matrix(rows,cols)
	for i in range(rows):
		for j in range(cols):
			a = amatrix.__getitem__([i,j])
			b = bmatrix.__getitem__([i,j])
			cmatrix.__setitem__([i,j],a+b)
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
	global VISUAL
	VISUAL = False
	global ITERATIONS
	ITERATIONS = -1

	global AMATRIX_LOAD,AMATRIX_SAVE,BMATRIX_LOAD,BMATRIX_SAVE
	AMATRIX_LOAD = None
	AMATRIX_SAVE = None
	BMATRIX_LOAD = None
	BMATRIX_SAVE = None
	
	try:
		opts,args = getopt.getopt(sys.argv[1:],"hvVi:", ["help","verbose","visual","iterations=","aload=","asave=","bload=","bsave="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt,arg in opts:
		if opt in ("-v","--verbose"):
			VERBOSE = True
		if opt in ("-V","--visual"):
			VISUAL = True
		if opt in ("-h","--help"):
			usage()
			sys.exit()
		if opt in ("-i", "--iterations"):
			ITERATIONS = int(arg)
		if opt == "--aload":
			AMATRIX_LOAD = arg
		if opt == "--asave":
			AMATRIX_SAVE = arg
		if opt == "--bload":
			BMATRIX_LOAD = arg
		if opt == "--bsave":
			BMATRIX_SAVE = arg

	global game
	game = Game()
	
	done = False
	while not done:
		game.update()
		done = game.control()
###
if __name__ == "__main__":
	main()
