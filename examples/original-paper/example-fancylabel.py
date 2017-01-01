#! /usr/bin/env python

from zplot import *
import sys
import random

# a simple label/arrow combination function
def label_with_arrow(canvas, x, y, text, size, anchor, dx, dy):
    ax, ay = x, y
    if anchor == 'top':
        ay = ay + size
    elif anchor == 'bottom':
        ay = ay - size
    else:
        print 'bad anchor'
        return
    canvas.text(coord=[x,y], anchor='c,c', size=size, text=text,
                bgcolor='white')
    canvas.line(coord=[[ax,ay],[dx,dy]], arrow=True)
    return

# a simple circle with inset text function
def circle_with_text(canvas, x, y, radius, fillcolor, text, size):
    canvas.circle(coord=[x,y], radius=radius, fill=True,
                  fillcolor=fillcolor, linewidth=0)
    canvas.text(coord=[x,y], text=text, size=size, anchor='c,c')
    return

# 
# main script
# 
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, 'example-fancylabel', dimensions=[600, 600])

random.seed(104)

for i in range(45):
    x, y = random.random() * 580 + 10, random.random() * 580 + 10
    circle_with_text(c, x, y, 7, 'lightgreen', 'g', 8)

label_with_arrow(c, 150, 60, 'Here is the orange one', 8, 'top', 254, 154)
circle_with_text(c, 270, 165, 7, 'orange', 'r', 8)

label_with_arrow(c, 240, 540, 'And here, the blue one', 8, 'bottom', 360, 430)
circle_with_text(c, 375, 420, 7, 'lightblue', 'b', 8)



c.render()
