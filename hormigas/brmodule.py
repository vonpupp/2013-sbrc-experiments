import boxmodule,pygame,time

def collide_down(mybox,boxes,container):
	collidebox = None
	collidetop = container[1]
	# Not necessary to check all boxes, if you check them by order packing order there is only a small set of possible collisions, I think.
	for box in boxes:
		if box.rect.top >= mybox.rect.bottom:
			if mybox.rect.left <= box.rect.left and mybox.rect.right >= box.rect.right:
				if box.rect.top < collidetop:
					collidetop = box.rect.top
					collidebox = box
			if mybox.rect.right <= box.rect.right and mybox.rect.left >= box.rect.left:
				if box.rect.top < collidetop:
					collidetop = box.rect.top
					collidebox = box
			if mybox.rect.left < box.rect.left and mybox.rect.right > box.rect.left:
				if box.rect.top < collidetop:
					collidetop = box.rect.top
					collidebox = box
			if mybox.rect.left < box.rect.right and mybox.rect.right > box.rect.right:
				if box.rect.top < collidetop:
					collidetop = box.rect.top
					collidebox = box
	return collidebox

def collide_right(mybox,boxes,container):
	collidebox = None
	collideleft = container[0]
	# Not necessary to check all boxes, if you check in reverse packing order, when you check collision against a box packed at the right border it's the last you have to check.
	for box in boxes:
		if box.rect.left >= mybox.rect.right:
			if mybox.rect.top <= box.rect.top and mybox.rect.bottom >= box.rect.bottom:
				if box.rect.left < collideleft:
					collideleft = box.rect.left
					collidebox = box
			if mybox.rect.bottom <= box.rect.bottom and mybox.rect.top >= box.rect.top:
				if box.rect.left < collideleft:
					collideleft = box.rect.left
					collidebox = box
			if mybox.rect.top < box.rect.top and mybox.rect.bottom > box.rect.top:
				if box.rect.left < collideleft:
					collideleft = box.rect.left
					collidebox = box
			if mybox.rect.top < box.rect.bottom and mybox.rect.bottom > box.rect.bottom:
				if box.rect.left < collideleft:
					collideleft = box.rect.left
					collidebox = box
	return collidebox
		
def slide_right(mybox,slidebox,boxes,container):
	# This could now be done by the boxmodule.put_out function?
	collidebox = collide_right(mybox,boxes,container)
	if slidebox == None:
		if collidebox != None:
			mybox.rect.left = collidebox.rect.left - mybox.rect.width
		else:
			mybox.rect.left = container[0] - mybox.rect.width
		return False
	else:
		if collidebox == None:
			if slidebox.rect.right + mybox.rect.width < container[0]:
				mybox.rect.left = slidebox.rect.right
				return True
			else:
				mybox.rect.left = container[0] - mybox.rect.width
				return False
		else:
			if collidebox.rect.left < slidebox.rect.right + mybox.rect.width:
				mybox.rect.left = collidebox.rect.left - mybox.rect.width
				return False
			else:
				mybox.rect.left = slidebox.rect.right
				return True
	return False

def pack_one(mybox,boxes,container):
	mybox.rect.topleft = (0,0 - mybox.rect.height)
	while True:
		collidebox = collide_down(mybox,boxes,container)
		if collidebox != None:
			mybox.rect.top = collidebox.rect.top - mybox.rect.height
		else:
			mybox.rect.top = container[1] - mybox.rect.height
		if not slide_right(mybox,collidebox,boxes,container):
			break
	if mybox.rect.top < 0:
		return False
	boxes.append(mybox)
	return True

def pack(boxes,container):
	solution = []
	myboxes = []
	for box in boxes:
		myboxes.append(box.copy())
	for box in myboxes:
		if pack_one(box,myboxes,container):
			solution.append(box)
		else:
			break
	return solution

def show(boxes,container):
	screen = pygame.display.set_mode(container)
	pygame.font.init()
	font = pygame.font.Font(None,16)
	n = 1
	for box in boxes:
		if box.rect.top >= 0 and box.rect.left >= 0:
			box.draw(screen)
			nsurf = font.render(str(n),True,(255,255,255))
			nrect = nsurf.get_rect()
			nrect.center = box.rect.center
			screen.blit(nsurf,nrect)
			n += 1
	end = False
	while not end:
		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == 12:
				end = True
				pygame.display.quit()
		time.sleep(1)

def stats(boxes,container):
	used_space = 0
	num_boxes = 0
	for box in boxes:
		if box.rect.top > 0:
			used_space += box.rect.height * box.rect.width
			num_boxes += 1
	percentage = float(used_space)/float(container[0]*container[1])
	print 'Used Space: ',used_space
	print '(',percentage*100.0,'% of ',container[0]*container[1],' points)'
	print 'Allocated Boxes: ',num_boxes
	return percentage

