import random,brmodule,boxmodule

def randtry(boxes,container,iterations):
	random.seed()
	max_used_space = 0
	for i in range(iterations):
		rand_boxes = []
		for box in boxes:
			rand_boxes.append(box.copy())
		rand_boxes = random.sample(rand_boxes,len(rand_boxes))
		solution = brmodule.pack(rand_boxes,container)
		used_space = brmodule.stats(solution,container)
		# To define: What is an optimum packing?
		if used_space > max_used_space:
			max_used_space = used_space
			best_solution = []
			for box in solution:
				best_solution.append(box.copy())
	return best_solution
