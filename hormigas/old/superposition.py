import matrix

def calc_matrix(boxes):
	x = 0
	for box in boxes:
		x = max(box.id,x)
	m = matrix.Matrix(x)
	for box1 in boxes:
		for box2 in boxes:
			area1 = box1.rect.height * box1.rect.width
			area2 = box2.rect.height * box2.rect.width
			area3 = min(box1.rect.height,box2.rect.height)*min(box1.rect.width,box2.rect.width)
			m.__setitem__((box1.id,box2.id),area1+area2-2*area3)
	return norm_matrix(m)

def norm_matrix(m):
	x = 0
	for i in range(m.cols()):
		for j in range(m.rows()):
			x = max(x,m.__getitem__((i,j)))
	for i in range(m.cols()):
		for j in range(m.rows()):
			value = m.__getitem((i,j))/x
			m.__setitem__((i,j),value)
	return m
