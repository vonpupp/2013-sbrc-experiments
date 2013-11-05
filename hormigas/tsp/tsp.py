#!/usr/bin/env python

import pygame, random, os, sys, matrix, getopt, math

#N = 6
TILESIZE = 64
SPEED = 4 # SPEED MUST BE A DIVISOR OF TILESIZE!!!!
#ANT_NUMBER = N**2
ALPHA = 1 # Relevance of the heuristics in choosing direction
BETA = 5 # Relevance of pheromones in choosing direction
GAMMA = 2.0 # Pheromone decay rate
DELTA = 10.0 # Path reinforcing factor

class LinkMatrix:

	'''For the sake of the printability I'm using N**2 points, 
	where the point n communicates with point n-1,n+1,n-N,n+N, 
	if displayed on a N**2 square adyacency matrix this results 
	on a 2-D net'''
	
	def __init__(self):
		self.matrix = matrix.Matrix(N**2)
		for i in range(N**2):
			'''As the matrix is going to be symmetric (my decision) I'm going 
			to use only the upper half of the matrix'''
			for j in (i+1,i+N):
				'''This condition prevents diagonal links from the last
				element of a column to the first in the next column'''
				if j == i+1 and j%N == 0:
					pass
				else:
					if j < N**2:
						link = Link(random.random(),0)
						self.matrix.__setitem__([i,j],link)
		self.steps = N**2

	def draw(self):
		game.screen.lock()
		for i in range(N**2):
			for j in (i+1,i+N):
				if j == i+1 and j%N == 0:
					pass
				else:
					if j < N**2:
						link = self.matrix.__getitem__([i,j])
						color = [0,0,link.pheromone*255]
						#Next line left commented: That's what you NEVER should do when programming, next time, please, do understandable code you inept
						#pygame.draw.line(game.screen,color,[(i%N)*TILESIZE+TILESIZE/2,(i/N)*TILESIZE+TILESIZE/2],[(j%N)*TILESIZE+TILESIZE/2,(j/N)*TILESIZE+TILESIZE/2],10-int(link.cost*10))
						# x = i%N, y = i/N
						origin = [(i%N)*TILESIZE+TILESIZE/2,(i/N)*TILESIZE+TILESIZE/2]
						destiny = [(j%N)*TILESIZE+TILESIZE/2,(j/N)*TILESIZE+TILESIZE/2]
						thickness = 10-int(link.cost*10)
						pygame.draw.line(game.screen,color,origin,destiny,thickness)
		game.screen.unlock()

	def getlink(self,nodes):
		if nodes[0] > nodes[1]:
			nodes = [nodes[1],nodes[0]]
		link = self.matrix.__getitem__(nodes) 
		return link

	def path_cost(self,path):
		total_cost = 0.0
		for node in range(len(path)-1):
			link = self.getlink([path[node],path[node+1]])
			total_cost += link.cost
		total_cost = total_cost / N**2
		return total_cost

	def pheromone_link(self, nodes, pheromone):
		link = self.getlink(nodes)
		'''We want a function for putting pheromone that has a maximum of 1, 
		minimum of 0, and slow growing at the end, a sinoidal of the sum 
		of the existent pheromone plus the injected pheromone seems nice'''
		#ToDo: Putting parameters into the pheromone function
		link.pheromone = math.sin(((link.pheromone+pheromone)*math.pi)/4)
		self.matrix.__setitem__(nodes,link)
		return link.pheromone

	def pheromone_path(self, path, pheromone):
		for node in range(len(path)-1):
			new_pheromone = self.pheromone_link([path[node],path[node+1]],pheromone)
		return new_pheromone

	def update(self):
		'''We want all the values in the pheromone matrix to decay 
		respect to GAMMA in N**2 steps of time, I'd like to do it in a continuous 
		function, but right now I've not the math skills for that'''
		'''Moreover, what I exactly need it's a radioactivity half life
		equation in differences'''
		self.steps -= 1
		if self.steps == 0:
			'''Next we have to think that we update the matrix TILESIZE/SPEED 
			times between each ant's decision (called a step), and that by
			now we want to change the pheromone matrix each N**2 steps'''
			self.steps = N**2*TILESIZE/SPEED
			for i in range(N**2):
				for j in (i+1,i+N):
					if j < N**2:
						link = self.matrix.__getitem__([i,j])
						if link != 0:
							link.pheromone = link.pheromone/GAMMA
							self.matrix.__setitem__([i,j],link)
					

class Link:
	
	def __init__(self, cost, pheromone = None):
		if pheromone is not None:
			self.pheromone = pheromone
		else:
			self.pheromone = 0.0
		self.cost = cost

	def update(self):
		pass

class Ant(pygame.sprite.Sprite):

	images = []

	def __init__(self, position = None):
		pygame.sprite.Sprite.__init__(self)
		if self.images == []:
			self.image, self.rect = load_image('ant_searching.gif')
			self.image.convert()
			self.images.append(self.image)
			self.image, self.rect = load_image('ant_carrying.gif')
			self.image.convert()
			self.images.append(self.image)
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		
		if position is None:
			self.position = random.randint(0,N**2-1)
		else:
			self.position = position
		self.rect.left = (self.position%N)*TILESIZE+TILESIZE/2-self.rect.width/2
		self.rect.top = (self.position/N)*TILESIZE+TILESIZE/2-self.rect.height/2

		self.moves = 0

		self.visited = []
		self.path = []
		for node in range(N**2):
			self.visited.append(False) 

	def possible_directions(self, position = None):
		if position == None:
			position = self.position
		#[-1,1,-N,N]
		directions = [1.0,1.0,1.0,1.0]
		if position%N == 0:
			directions[0] = 0.0
		else:
			if self.visited[position - 1]:
				directions[0] = 0.0
		if position%N == N-1:
			directions[1] = 0.0
		else:
			if self.visited[position + 1]:
				directions[1] = 0.0
		if position < N:
			directions[2] = 0.0
		else:
			if self.visited[position - N]:
				directions[2] = 0.0
		if position >= N**2-N:
			directions[3] = 0.0
		else:
			if self.visited[position + N]:
				directions[3] = 0.0
		options = 0
		for direction in directions:
			if direction:
				options += 1
		if options > 0:
			for direction in range(len(directions)):
				directions[direction] = directions[direction]/options
		return directions
			
	def less_cost_directions(self):
		costs = [0.0,0.0,0.0,0.0]
		possible_directions = self.possible_directions()
		for direction in range(len(possible_directions)):
			if possible_directions[direction] != 0.0:
				if direction == 0:
					node = -1
				if direction == 1:
					node = 1
				if direction == 2:
					node = -N
				if direction == 3:
					node = N
				link = game.linkmatrix.getlink([self.position, self.position + node])
				costs[direction] = 1 - link.cost
		costs = normalize(costs)
		return costs

	def less_grade_directions(self):
		grades = [4.0,4.0,4.0,4.0]
		possible_directions = self.possible_directions()
		for direction in range(len(possible_directions)):
			if possible_directions[direction] != 0.0:
				if direction == 0:
					node = -1
				if direction == 1:
					node = 1
				if direction == 2:
					node = -N
				if direction == 3:
					node = N
				neighbour_directions = self.possible_directions(self.position + node) 
				for link in neighbour_directions:
					if link:
						grades[direction] -= 1
			else:
				grades[direction] = 0.0
		grades = normalize(grades)
		return grades
		
	def pheromone_directions(self):
		pheromones = [0.0,0.0,0.0,0.0]
		possible_directions = self.possible_directions()
		for direction in range(len(possible_directions)):
			if possible_directions[direction] != 0.0:
				if direction == 0:
					node = -1
				if direction == 1:
					node = 1
				if direction == 2:
					node = -N
				if direction == 3:
					node = N
				link = game.linkmatrix.getlink([self.position, self.position + node])
				pheromones[direction] = link.pheromone
		pheromones = normalize(pheromones)
		return pheromones

	def choose_direction(self):
		less_cost_directions = self.less_cost_directions()
		pheromone_directions = self.pheromone_directions()
		less_grade_directions = self.less_grade_directions()
		directions = [0.0,0.0,0.0,0.0]
		if pheromone_directions != [0.0,0.0,0.0,0.0]:
			for direction in range(len(directions)):
				directions[direction] = (less_cost_directions[direction]*ALPHA)*(pheromone_directions[direction]*BETA)
		else:
			#directions = less_cost_directions
			directions = less_grade_directions
		directions = normalize(directions)
		if directions == [0.0,0.0,0.0,0.0]:
			if len(self.path) == N**2:
				cost = game.linkmatrix.path_cost(self.path)
				if VERBOSE:
					#print "Solution found!"
					#print self.path, cost
					print game.iterations, cost
				pheromone = math.cos((cost**DELTA*math.pi)/2.0)
				game.linkmatrix.pheromone_path(self.path,pheromone)
			for node in range(len(self.visited)):
				self.visited[node] = False
			self.path = []
			return 0
		else:
			election = random.random()
			for direction in range(len(directions)):
				election -= directions[direction]
				if election < 0:
					if direction == 0:
						return -1
					if direction == 1:
						return 1
					if direction == 2:
						return -N
					if direction == 3:
						return N
			
	def move(self):
		if self.direction == -1:
			self.rect.left -= SPEED
		if self.direction == 1:
			self.rect.left += SPEED
		if self.direction == -N:
			self.rect.top -= SPEED
		if self.direction == N:
			self.rect.top += SPEED
		return True
		

	def update(self):
		if self.moves == 0:
			self.path.append(self.position)
			self.visited[self.position] = True
			self.direction = self.choose_direction()
			'''Protection mechanism for avoiding a trapped ant 
			(which doesn't return a direction) to continue moving,
			to be done in good way'''
			if not self.direction:
				return False
			self.position = self.position + self.direction
			self.moves = TILESIZE/SPEED
		else:
			self.move()
			self.moves -= 1
		return True

class Game:

	screen = None
	linkmatrix = None
	ant_sprites = None
	iterations = None
	steps = None

	def __init__(self):
		random.seed()
		pygame.init()

		self.screen = pygame.display.set_mode([N*TILESIZE,N*TILESIZE])
		self.linkmatrix = LinkMatrix()

		self.ant_sprites = pygame.sprite.RenderUpdates()
		for ant in range(ANT_NUMBER):
			self.ant_sprites.add(Ant())
		pygame.display.set_caption("Ant-TSP")
		
		self.iterations = 0
		self.steps = 0

	def control(self):
		for e in pygame.event.get():
			if e.type == 12:
				return True
		return False

	def update(self):

		if self.steps == 0:
			self.steps == TILESIZE/SPEED
			self.iterations += 1
		else:
			self.steps -=1

		self.screen.fill((255,255,255))
		
		self.linkmatrix.update()
		self.linkmatrix.draw()
		
		self.ant_sprites.update()
		self.ant_sprites.draw(self.screen)
		
		pygame.display.flip()

		return True

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

	global N
	N = 6

	try:
		opts,args = getopt.getopt(sys.argv[1:],"hvn:", ["help","verbose"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt,arg in opts:
		if opt == "-n":
			N = int(arg)
		if opt in ("-v","--verbose"):
			VERBOSE = True
		if opt in ("-h","-help"):
			usage()
			sys.exit()

	global ANT_NUMBER
	ANT_NUMBER = N**2

	global game
	game = Game()
	
	done = False
	while not done:
		game.update()
		done = game.control()

if __name__ == "__main__":
	main()
