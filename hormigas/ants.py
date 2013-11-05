import brmodule, boxmodule, random, matrix

ALPHA = 500.0
BETA = 1.0

class Ant:
	
	def __init__(self, boxes, container):
		self.solution = []
		self.boxes = []
		self.container = container
		for box in boxes:
			self.boxes.append(box.copy())
	
	def calc_probs(self,box):
		ph = graph.__getitem__((len(self.solution), box.id))
		he = 1.0
		return ph**ALPHA + he**BETA

	def pack(self):
		probabilities = []
		for box in self.boxes:
			probabilities.append(self.calc_probs(box))
		probabilities = normalize(probabilities)
		election = random.random()
		for i in range(len(probabilities)):
			election -= probabilities[i]
			if election < 0.0:
				packed = brmodule.pack(self.boxes[i],self.solution,self.container)
				if not packed:
					return False
				self.boxes = self.boxes[:i]+self.boxes[(i+1):]
				break
		if self.boxes == []:
			return False
		return True

	def solution(self):
		return self.solution

class Graph(matrix.Matrix):
	
	def reinforce(self,boxes):
		for i in range(len(boxes)):
			value = self.__getitem__((boxes[i].id,i))
			self.__setitem__((boxes[i].id,i),value + 1.0)
			
	def decay(self):
		for i in range(self.cols()):
			for j in range(self.rows()):
				value = self.__getitem__((i,j))
				self.__setitem__((i,j),0.0)

def graph2boxes(graph,boxes):
	myboxes = []
	for j in range(graph.cols()):
		max = 0
		box_id = None
		for i in range(graph.rows()):
			value = graph.__getitem__((i,j))
			if value > max:
				box_id = i
				max = value
		for box in boxes:
			if box.id == box_id:
				myboxes.append(box.copy())
				break
	return myboxes

def pack(boxes, container, num_ants, max_ants):

	import draw,pygame
	s = draw.open_window()

	myboxes = []
	for box in boxes:
		myboxes.append(box.copy())
	
	global graph
	graph = Graph(len(myboxes))
	
	ants = []
	while max_ants != 0 or ants != []:
		for i in range(num_ants):
			ants.append(Ant(myboxes, container))
			max_ants -= 1
		solutions = []
		while ants != []:
			i = 0
			while i < len(ants):
				working = ants[i].pack()
				if not working:
					solutions.append(ants[i].solution)
					ants = ants[:i]+ants[(i+1):]
				else:
					i += 1
		graph.decay()
		for solution in solutions:
			graph.reinforce(solution)

		draw.draw_nodes(s,graph)
		draw.draw_links(s,graph)
		pygame.display.update()

	return graph

def normalize(vector):
	total = 0
	for x in vector:
		total += x
	if total != 0:
		for position in range(len(vector)):
			vector[position] = vector[position]/total
	return vector
