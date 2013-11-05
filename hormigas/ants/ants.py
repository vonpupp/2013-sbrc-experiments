#!/usr/bin/env python

import pygame, random, os, sys, matrix, getopt


class Food(pygame.sprite.Sprite):

	def __init__(self, power, position = None):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('food.gif')
		if position == None:
			position = [random.randint(0,WINSIZE[0]-self.rect.width), random.randint(0,WINSIZE[1]-self.rect.height)]
		self.rect.topleft = position
		self.power = power
		
	def take(self,quantity):
		if quantity > self.power:
			quantity = self.power
		self.power -= quantity
		return quantity

	def update(self):
		if self.power == 0:
			self.kill()
	
class Nest(pygame.sprite.Sprite):
	
	image = None
	
	def __init__(self, position=None):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('nest-big.gif')
		if position == None:
			position = [random.randint(0,WINSIZE[0]-64), random.randint(0,WINSIZE[1]-64)]
		self.rect.topleft = position

	def draw(self):
		game.screen.blit(self.image, self.rect)
	
	def update(self):
		pass

class Pheromone(pygame.sprite.Sprite):

	def __init__(self, power, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([TILE_SIZE,TILE_SIZE])
		r = 200 - power
		g = 250 - power
		b = 150 + power
		if r < 0: r = 0
		if g < 0: g = 0
		if b > 255: b = 255
		self.image.fill([r,g,b])
		self.rect = self.image.get_rect()
		self.rect.topleft = position

class PheromoneMatrix:

	pheromone_list = []

	def __init__(self):
		self.pheromones = matrix.Matrix(WINSIZE[0]/TILE_SIZE,WINSIZE[1]/TILE_SIZE)
		
	def check(self,position):
		i = int(position[0]/TILE_SIZE)
		j = int(position[1]/TILE_SIZE)
		if i >= WINSIZE[0]/TILE_SIZE or j >= WINSIZE[1]/TILE_SIZE:
			return 0
		if i <= 0 or j <= 0:
			return 0
		pheromone_value = self.pheromones.__getitem__([i,j])
		return pheromone_value	
	
	def empower(self,power,position):
		i = int(position[0]/TILE_SIZE)
		j = int(position[1]/TILE_SIZE)
		pheromone_value = self.pheromones.__getitem__([i,j])
		if pheromone_value > 0:
			power += pheromone_value
		self.pheromones.__setitem__([i,j],power)
		
	def draw(self):
		for pheromone in self.pheromone_list:
			self.pheromone_list.remove(pheromone)
			pheromone.kill()
		for i in range(self.pheromones.rows()):
			for j in range(self.pheromones.cols()):
				power = self.pheromones.__getitem__([i,j])
				if power > 0:
					power = power
					position = [i*TILE_SIZE,j*TILE_SIZE]
					pheromone = Pheromone(power, position)
					self.pheromone_list.append(pheromone)
					game.screen.blit(pheromone.image, pheromone.rect)
				
	def update(self): #decay
		for i in range(self.pheromones.rows()):
			for j in range(self.pheromones.cols()):
				pheromone_value = self.pheromones.__getitem__([i,j])
				if pheromone_value > 10:
					pheromone_value -= 1 #This could be a more advanced function of decay
				self.pheromones.__setitem__([i,j],pheromone_value)

class Ant(pygame.sprite.Sprite):

	images = []

	def __init__(self, position = None):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ant_searching.gif')
		self.images.append(self.image)
		self.image, self.rect = load_image('ant_carrying.gif')
		self.images.append(self.image)
		self.image = self.images[0]
		
		if position == None:
			#---Random positioning of the ant---#
			self.rect.left = random.randint(0,WINSIZE[0]-self.rect.width)
			self.rect.top = random.randint(0,WINSIZE[1]-self.rect.height)
		
		self.action = "search"
		self.selected = False
		self.direction = [0,0]
		self.timer = 0

	def choose_direction(self):

		max = 0
		if self.action == "search":
			direction = [0,0]
			nest_direction = self.nest_direction()
			
			for i in -1,0,1:
				for j in -1,0,1:
					if [i,j] != [0,0] and i != nest_direction[0] and j != nest_direction[1]:
						tmp = game.pheromone_matrix.check([self.rect.center[0]+i*self.rect.width,self.rect.center[1]+j*self.rect.height])
						if tmp > max:
							max = tmp
							direction = [i,j]
			self.direction = direction
	
		if self.action == "return":
			self.direction = self.nest_direction()
			
		if random.random() < 0.1 or self.direction == [0,0]:
			self.direction = [random.randint(-1,1),random.randint(-1,1)]
	
	def nest_direction(self):
		direction = [0,0]
		if game.nest.rect.left > self.rect.left:
			direction[0] = 1
		if game.nest.rect.top > self.rect.top:
			direction[1] = 1
		if game.nest.rect.right < self.rect.right:
			direction[0] = -1
		if game.nest.rect.bottom < self.rect.bottom:
			direction[1] = -1
		return direction
		

	def in_nest(self):
		if game.nest.rect.left > self.rect.left:
			return False
		if game.nest.rect.top > self.rect.top:
			return False
		if game.nest.rect.right < self.rect.right:
			return False
		if game.nest.rect.bottom < self.rect.bottom:
			return False
		return True	

	def update(self):
		
		action = self.action
		
		if self.timer == 0:
			self.timer = random.randint(1,64)
			self.choose_direction()
		self.timer -= 1

		if self.rect.bottom == WINSIZE[1] and self.direction[1] == 1:
			self.direction[1] = 0
		if self.rect.right == WINSIZE[0] and self.direction[0] == 1:
			self.direction[0] = 0
		if self.rect.top == 0 and self.direction[1] == -1:
			self.direction[1] = 0
		if self.rect.left == 0 and self.direction[0] == -1:
			self.direction[0] = 0

		self.rect.left += self.direction[0]
		self.rect.top += self.direction[1]

		if self.in_nest():
			self.image = self.images[0]
			self.action = "search"

		if self.action == "search" or self.action == "follow":
			food = pygame.sprite.spritecollideany(self,game.food_sprites)
		
			if food is not None:
				self.action = "return"
				self.image = self.images[1]
				food.take(1)

		if self.action == "return":
			game.pheromone_matrix.empower(20, self.rect.center)

		if self.selected == True and action != self.action:
			print self.action

class Game:

	screen = None
	background = None
	ant_sprites = None
	pheromone_matrix = None
	nest = None
	
	def __init__(self):
		random.seed()
		pygame.init()
		
		self.screen = pygame.display.set_mode(WINSIZE)
		pygame.display.set_caption("Hormigas")
		
		self.background = pygame.Surface(WINSIZE)
		self.background.fill((200,250,150))
		
		self.ant_sprites = pygame.sprite.RenderUpdates()
		for ant in range(ANT_NUMBER):
			self.ant_sprites.add(Ant())

		self.food_sprites = pygame.sprite.RenderUpdates()
		for food_source in range(FOOD_NUMBER):
			self.food_sprites.add(Food(1000))

		self.load(INI_FILE)

		self.pheromone_matrix = PheromoneMatrix()

		self.nest = Nest()
		
	def load(self,file):
		pass
		
	
	def control(self):
		for e in pygame.event.get():
			if e.type == 12:
				return True
			if e.type == 3:
				if e.key == 113:
					return True
			if e.type == 6:
				if e.button == 1:
					game.select(e.pos)
		return False
		
	def select(self,position):
		for ant in game.ant_sprites.sprites():
			ant.selected = False
			if game.point(position, ant.rect):
				ant.selected = True

	def point(self, position, rect):
		if rect.left > position[0]:
			return False
		if rect.right < position[0]:
			return False
		if rect.top > position[1]:
			return False
		if rect.bottom < position[1]:
			return False
		return True	
		
	'''def collide(self, rect1, rect2):
		if rect1.left > rect2.left:
			return False
		if rect1.top > rect2.top:
			return False
		if rect1.right < rect2.right:
			return False
		if rect1.bottom < rect2.bottom:
			return False
		return True'''	


	def update(self):
		self.screen.blit(self.background, (0,0))
		
		self.pheromone_matrix.update()
		self.pheromone_matrix.draw()
		
		self.ant_sprites.update()
		self.ant_sprites.clear(self.screen, self.background)
		self.ant_sprites.draw(self.screen)

		self.food_sprites.update()
		self.food_sprites.clear(self.screen, self.background)
		self.food_sprites.draw(self.screen)

		self.nest.update()
		self.nest.draw()

		pygame.display.flip()

		return True

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
	
	global WINSIZE
	WINSIZE = [800,608]
	global ANT_NUMBER
	ANT_NUMBER = 20
	global FOOD_NUMBER
	FOOD_NUMBER = 4
	global TILE_SIZE
	TILE_SIZE = 32
	global INI_FILE
	INI_FILE = "hormigas.ini"
	global VERBOSE
	VERBOSE = False

	try:
		opts,args = getopt.getopt(sys.argv[1:], "hi:w:a:f:v", ["help", "inifile=", "winsize=","antnumber=","foodnumber=", "verbose"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for o,a in opts:
		if o in ("-v", "--verbose"):
			VERBOSE = True
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		if o in ("-i", "--inifile"):
			INI_FILE = int(a)
		if o in ("-w", "--winsize"):
			#WINSIZE = a
			pass
		if o in ("-a", "--antnumber"):
			ANT_NUMBER = int(a)
		if o in ("-f", "--foodnumber"):
			FOOD_NUMBER = int(a)

	global game
	game = Game()

	done = False
	while not done:
		game.update()
		done = game.control()

if __name__ == "__main__":
	
	main()
	
