import pygame

WINSIZE = [512,512]
TILESIZE = 8

def open_window():
	screen = pygame.display.set_mode(WINSIZE)
	return screen

def close_window():
	pygame.display.quit()
	
def clear(screen):
	screen.fill((255,255,255))
	
def draw_nodes(screen, matrix):
	clear(screen)
	screen.lock()
	for i in range(matrix.cols()):
		for j in range(matrix.rows()):
			color = [0,0,0]
			position = [TILESIZE*(i+1),TILESIZE*(j+1)]
			pygame.draw.circle(screen, color, position, 2, 0)
	screen.unlock()

def draw_links(screen, matrix):
	screen.lock()
	cols = matrix.cols()
	rows = matrix.rows()
	for i in range(cols):
		for j in range(rows):
			if i < rows-1:
				for k in range(cols):
					value_start = matrix.__getitem__([j,i])
					value_end = matrix.__getitem__([k,i+1])
					if value_start > 0.0 and value_end > 0.0:
						color = [0,255,0]
						start = [TILESIZE*(i+1),TILESIZE*(j+1)]
						end = [TILESIZE*(i+2),TILESIZE*(k+1)]
						thickness = 2 # Will be proportional to the cost of the link
						pygame.draw.line(screen,color,start,end,thickness)
	screen.unlock()

def help():
	print "def draw_links(screen, matrix):"
	print "def draw_nodes(screen, matrix):"
	print "def clear(screen):"
	print "def close_window():"
	print "def open_window():return screen"
