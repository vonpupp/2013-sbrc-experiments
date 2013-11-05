#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

WINSIZE = [800,608]
ANT_NUMBER = 20

class Ant(pygame.sprite.Sprite):

	images = []

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ant_searching.gif')
		self.images.append(self.image)
		self.image, self.rect = load_image('ant_carrying.gif')
		self.images.append(self.image)
		self.position = [None,None]
		self.image = self.images[0]
	
class Game:

	screen = None
	background = None
	ant_sprites = None
	
	def __init__(self):
		random.seed()
		pygame.init()
		
		self.screen = pygame.display.set_mode(WINSIZE)
		pygame.display.set_caption("Hormigas")
		
		self.background = pygame.Surface(WINSIZE)
		self.background.fill((0,0,0))
		
		self.ant_sprites = pygame.sprite.RenderUpdates()
		for ant in range(ANT_NUMBER):
			self.ant_sprites.add(Ant())
		
	def update(self):
		self.screen.blit(self.background, (0,0))
		
		self.ant_sprites.update()
		self.ant_sprites.clear(self.screen, self.background)
		self.ant_sprites.draw(self.screen)

		pygame.display.flip()
		

class Interface:
	
	def __init__(self):
		# This procedure creates the interface window, with all the attributes and buttons
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.go_button = gtk.Button("Go")
		self.go_button.connect("clicked", self.go)
		self.window.add(self.button)
		self.button.show()
		self.window.show()

	def delete_event(self, widget, event, data = None):
		# Cancel an ongoing event
		return gtk.FALSE

	def destroy(self, widget, data = None):
		gtk.main_quit()

	def go(self, widget, data = None):
		if self.go_button.get_label() == "Go":
			self.go_button.set_label("Stop")
		else:
			self.button.set_label("Go")
		# Let Hormigas go for another step
		pass

	def main(self):
		# Main loop
		gtk.main()

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

if __name__ == "__main__":
	interface = Interface()
	interface.main()
