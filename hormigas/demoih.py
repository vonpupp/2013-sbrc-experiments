import boxmodule,brmodule
b = boxmodule.random_boxes(100,16,64)
c = 256,512
import order
bih = order.ih(b) 
sih = brmodule.pack(bih,c)
brmodule.show(sih,c)

