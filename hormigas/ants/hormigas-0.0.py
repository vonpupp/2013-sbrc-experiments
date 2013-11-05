#!/usr/bin/env python

import pygame, os, sys, random, math
from pygame.locals import *
from random import randint

WINSIZE = [800,608]
FPS = 60
ANT_NUMBER = 20
FOOD_NUMBER = 3

class Food(pygame.sprite.Sprite):

	def __init__(self, power, position):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('food.gif')
		self.rect[0] = position[0]
		self.rect[1] = position[1]
		self.power = power
		
	def take(quantity):
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
		self.image, self.rect = load_image('pheromone.gif')
		self.rect[0] = position[0]
		self.rect[1] = position[1]
		self.power = power
		
	def empower(self,power):
		self.power += power
		if self.power > 255:
			self.power = 255	
		
	def update(self):
		if self.power > 0:
			self.power -= 1
		if self.power == 0:
			self.kill()
		self.image.fill([0,0,255-self.power])

class Nest(pygame.sprite.Sprite):
	
	image = None
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('nest-big.gif')
		self.position = [WINSIZE[0]/2, WINSIZE[1]/2]
		self.rect[0] = self.position[0]
		self.rect[1] = self.position[1]
	
	def update(self):
		pass

class Ant(pygame.sprite.Sprite):

	images = []
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ant.gif')
		self.position = [None,None]
		free = False
		while free == False:
			self.position[0] = random.randint(0,WINSIZE[0]/32-1)*32
			self.position[1] = random.randint(0,WINSIZE[1]/32-1)*32
			self.rect[0] = self.position[0]
			self.rect[1] = self.position[1]
			collisions = pygame.sprite.spritecollide(self,ant_sprites,False)
			if len(collisions) == 0:
				free = True
		self.action = "none"
		self.direction = [0,0]
		#print "Ant created at "+str(self.rect[0])+","+str(self.rect[1])

	def choose_direction(self):
		self.direction[0] = 0
		self.direction[1] = 0
		while self.direction[0] == self.direction[1] == 0:
			self.direction[0] = random.randint(-1,1)
			self.direction[1] = random.randint(-1,1)
			if self.direction[0] == -1 and self.position[0] == 0:
				self.direction[0] = 0
			if self.direction[1] == -1 and self.position[1] == 0:
				self.direction[1] = 0
			if self.direction[0] == 1 and self.position[0] >= WINSIZE[0]-32:
				self.direction[0] = 0
			if self.direction[1] == 1 and self.position[1] >= WINSIZE[1]-32:
				self.direction[1] = 0

	def update(self):
		if self.action == "move" and self.position[0] % 32 == 0 and self.position[1] % 32 == 0:
			self.action = "none"
			
		if self.action == "none":
			self.action = "move"
			self.choose_direction()
			pheromones = pygame.sprite.spritecollide(self,pheromone_sprites,False)
			if len(pheromones) > 0:
				pheromones[0].empower(100)
			else:
				pheromone_sprites.add(Pheromone(100, [self.position[0],self.position[1]]))

		if self.action == "move":
			self.position[0] += self.direction[0]
			self.position[1] += self.direction[1]

			#Check collisions (not when in the nest)
			if pygame.sprite.spritecollide(self,nest_sprites,False) == []:
				collisions = pygame.sprite.spritecollide(self,ant_sprites,False)
				if len(collisions) > 1:
					self.direction[0] = -self.direction[0]
					self.direction[1] = -self.direction[1]
					self.position[0] += 2*self.direction[0]
					self.position[1] += 2*self.direction[1]

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
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption("Hormigas")

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((200, 250, 150))
	
	global food_sprites
	food_sprites = pygame.sprite.RenderUpdates()
	for food in range(FOOD_NUMBER):
		food_sprites.add(Food(randint(1,100),[randint(0,WINSIZE[0]),randint(0,WINSIZE[1])]))
	
	global pheromone_sprites
	pheromone_sprites = pygame.sprite.RenderUpdates()
	pheromone_sprites.add(Pheromone(255,[0,0]))

	global nest_sprites
	nest_sprites = pygame.sprite.RenderUpdates()
	nest_sprites.add(Nest())

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
		
		pheromone_sprites.update()
		pheromone_sprites.clear(screen, background)
		pheromone_sprites.draw(screen)
				
		food_sprites.update()
		food_sprites.clear(screen, background)
		food_sprites.draw(screen)
				
		nest_sprites.update()
		nest_sprites.clear(screen, background)
		nest_sprites.draw(screen)
		
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
