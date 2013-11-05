# Randtry demo
import boxmodule,ants
b = boxmodule.load_boxes('boxes1')
c = [256,512]
g = ants.pack(b,c,2,10)
b2 = ants.graph2boxes(g,b)
import pack
pack.pack(b2,c)
pack.show(b2,c)
