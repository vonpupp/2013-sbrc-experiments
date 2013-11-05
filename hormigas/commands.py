

import boxmodule, ants
b = boxmodule.load_boxes('boxes1')
c = [256,512]
g = ants.pack(b,c,2,20)

import draw, pygame, matrix
pygame.init()
s = draw.open_window()
draw.draw_nodes(s,g)
draw.draw_links(s,g)
pygame.display.update()
