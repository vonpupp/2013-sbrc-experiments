def dw(boxes):
	myboxes = []
	for box in boxes:
		i = 0
		while i < len(myboxes):
			if box.rect.width > myboxes[i].rect.width:
				myboxes = myboxes[:i]+[box.copy()]+myboxes[i:]
				break
			i += 1
		if i == len(myboxes):
			myboxes.append(box.copy())
	return myboxes

def dh(boxes):
	myboxes = []
	for box in boxes:
		i = 0
		while i < len(myboxes):
			if box.rect.height > myboxes[i].rect.height:
				myboxes = myboxes[:i]+[box.copy()]+myboxes[i:]
				break
			i += 1
		if i == len(myboxes):
			myboxes.append(box.copy())
	return myboxes

def iw(boxes):
	myboxes = []
	for box in boxes:
		i = 0
		while i < len(myboxes):
			if box.rect.width < myboxes[i].rect.width:
				myboxes = myboxes[:i]+[box.copy()]+myboxes[i:]
				break
			i += 1
		if i == len(myboxes):
			myboxes.append(box.copy())
	return myboxes

def ih(boxes):
	myboxes = []
	for box in boxes:
		i = 0
		while i < len(myboxes):
			if box.rect.height < myboxes[i].rect.height:
				myboxes = myboxes[:i]+[box.copy()]+myboxes[i:]
				break
			i += 1
		if i == len(myboxes):
			myboxes.append(box.copy())
	return myboxes
