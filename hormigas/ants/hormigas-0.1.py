#!/usr/bin/env python

import pygame, os, sys, random, math, matrix
from pygame.locals import *
from random import randint
from matrix import Matrix

WINSIZE = [800,608]
FPS = 60
ANT_NUMBER = 10
FOOD_NUMBER = 3

class Food(pygame.sprite.Sprite):

	def __init__(self, power, position):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('food.gif')
		self.rect[0] = position[0]
		self.rect[1] = position[1]
		self.power = power
		
	def take(self,quantity):
		if quantity > self.power:
			quantity = self.power
		self.power -= quantity
		return quantity

	def update(self):
		if self.power == 0:
			self.kill()

class Pheromone(pygame.sprite.Sprite):

	def __init__(self, power, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([32,32])
		if power > 255: power = 255
		self.image.fill([0,0,255-power])
		self.rect = self.image.get_rect()
		self.rect.topleft = position

class PheromoneMatrix:

	pheromone_list = []

	def __init__(self):
		self.pheromones = Matrix(WINSIZE[0]/32,WINSIZE[1]/32)
		
	def check(self,position):
		i = int(position[0]/32)
		j = int(position[1]/32)
		if i >= WINSIZE[0]/32 or j >= WINSIZE[1]/32:
			return 0
		if i <= 0 or j <= 0:
			return 0
		pheromone_value = self.pheromones.__getitem__([i,j])
		return pheromone_value	
	
	def empower(self,power,position):
		i = int(position[0]/32)
		j = int(position[1]/32)
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
					position = [i*32,j*32]
					pheromone = Pheromone(power, position)
					self.pheromone_list.append(pheromone)
					screen.blit(pheromone.image, pheromone.rect)
				
	def update(self): #decay
		for i in range(self.pheromones.rows()):
			for j in range(self.pheromones.cols()):
				pheromone_value = self.pheromones.__getitem__([i,j])
				if pheromone_value > 0:
					pheromone_value -= 1 #This could be a more advanced function of decay
				self.pheromones.__setitem__([i,j],pheromone_value)

class Nest(pygame.sprite.Sprite):
	
	image = None
	
	def __init__(self, position=None):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('nest-big.gif')
		if position == None:
			self.position = [WINSIZE[0]/2, WINSIZE[1]/2]
		else:
			self.position = position
		self.rect[0] = self.position[0]
		self.rect[1] = self.position[1]

	def draw(self):
		screen.blit(self.image, self.rect)
	
	def update(self):
		pass

class Ant(pygame.sprite.Sprite):

	'''
	Actions:
		Search Food
		Return to the Nest
	'''

	images = []
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ant.gif')
		self.image.convert()
		self.images.append(self.image)
		self.image, self.rect = load_image('ant_working.gif')
		self.image.convert()
		self.images.append(self.image)
		self.position = [None,None]
		self.image = self.images[0]
		
		#---Random positioning of the ant---#
		free = False
		while free == False:
			self.position[0] = random.randint(0,WINSIZE[0]/32-1)*32
			self.position[1] = random.randint(0,WINSIZE[1]/32-1)*32
			self.rect[0] = self.position[0]
			self.rect[1] = self.position[1]
			collisions = pygame.sprite.spritecollide(self,ant_sprites,False)
			if len(collisions) == 0:
				free = True
		
		self.action = "search"
		self.direction = [0,0]

	def choose_direction(self):
		
		if self.action == "search":
			#---To be transformed into a serious way to walk, by now it's random
			if random.random() < 0.3:
				self.direction[0] = random.randint(-1,1)
				self.direction[1] = random.randint(-1,1)
			else:
				self.direction = [0,0]
				if nest.rect[0] > self.rect[0]:
					self.direction[0] = -1
				if nest.rect[0] < self.rect[0]:
					self.direction[0] = 1
				if nest.rect[1] > self.rect[1]:
					self.direction[1] = -1
				if nest.rect[1] < self.rect[1]:
					self.direction[1] = 1
				#---Now we have the general direction we want, let's check the pheromones
				a = pheromone_matrix.check([self.position[0]+32*self.direction[0],self.position[1]+32*self.direction[0]])
				b = pheromone_matrix.check([self.position[0]+32*self.direction[0],self.position[1]])
				c = pheromone_matrix.check([self.position[0],self.position[1]+32*self.direction[0]])
				if a > b and a > c:
					pass
				if b > a and b > c:
					self.direction[1] = 0
				if c > b and c > a:
					self.direction[0] = 0

				
		if self.action == "return":
			self.direction = [0,0]
			if nest.rect[0] > self.rect[0]:
				self.direction[0] = 1
			if nest.rect[0] < self.rect[0]:
				self.direction[0] = -1
			if nest.rect[1] > self.rect[1]:
				self.direction[1] = 1
			if nest.rect[1] < self.rect[1]:
				self.direction[1] = -1
		#---Taking care of remaining on the window
		if self.direction[0] == -1 and self.position[0] == 0:
			self.direction[0] = 0
		if self.direction[1] == -1 and self.position[1] == 0:
			self.direction[1] = 0
		if self.direction[0] == 1 and self.position[0] >= WINSIZE[0]-32:
			self.direction[0] = 0
		if self.direction[1] == 1 and self.position[1] >= WINSIZE[1]-32:
			self.direction[1] = 0
		

	def update(self):

		pheromone_matrix.empower(5,self.rect.center)

		if self.position[0] % 32 == 0 and self.position[1] % 32 == 0:
			self.choose_direction()
			
		self.position[0] += self.direction[0]
		self.position[1] += self.direction[1]

		#Check collisions (not when in the nest)
		if pygame.sprite.spritecollide(self,nest_sprites,False) == []:
			collisions = pygame.sprite.spritecollide(self,ant_sprites,False)
			'''if len(collisions) > 1:
				self.direction[0] = -self.direction[0]
				self.direction[1] = -self.direction[1]
				self.position[0] += 2*self.direction[0]
				self.position[1] += 2*self.direction[1]'''
		else:
			self.image = self.images[0]
			self.action = "search"

		food = pygame.sprite.spritecollideany(self,food_sprites)
		
		if food is not None:
			self.action = "return"
			self.image = self.images[1]
			food.take(1)

		self.rect[0] = self.position[0]
		self.rect[1] = self.position[1]
	
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

def main():

	random.seed()

	pygame.init()

	global screen
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption("Hormigas")

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((200, 250, 150))
	
	global pheromone_matrix 
	pheromone_matrix = PheromoneMatrix()
	
	global food_sprites
	food_sprites = pygame.sprite.RenderUpdates()
	for food in range(FOOD_NUMBER):
		food_sprites.add(Food(100000,[randint(0,WINSIZE[0]),randint(0,WINSIZE[1])]))
	
	global nest
	global nest_sprites
	nest = Nest()
	nest_sprites = pygame.sprite.Group(nest)

	global ant_sprites
	ant_sprites = pygame.sprite.RenderUpdates()
	for ant in range(ANT_NUMBER):
		ant_sprites.add(Ant())

	screen.blit(background, (0,0))
	pygame.display.flip()

	clock = pygame.time.Clock()

	done = 0
	while not done:
		
		clock.tick(FPS)
		
		screen.blit(background, (0,0))
		
		pheromone_matrix.update()
		pheromone_matrix.draw()
		
		food_sprites.update()
		food_sprites.clear(screen, background)
		food_sprites.draw(screen)
				
		nest.update()
		nest.draw()
		
		ant_sprites.update()
		ant_sprites.clear(screen, background)
		ant_sprites.draw(screen)
		
		pygame.display.flip()
		
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYUP and e.key == K_q):
				done = 1
				break

if __name__ == "__main__":
	main()
