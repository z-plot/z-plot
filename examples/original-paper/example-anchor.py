#! /usr/bin/env python

from zplot import *

# describe the drawing surface
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='example-anchor', dimensions=[200, 60])

y = 10 
s = 20

x = 10
c.text(coord=[x,y], anchor='l,l', text='Anchor Is l,l', size=10)
c.text(coord=[x,y+s], anchor='l,c', text='Anchor Is l,c', size=10)
c.text(coord=[x,y+s+s], anchor='l,h', text='Anchor Is l,h', size=10)

c.circle(coord=[x,y], linecolor='red', fill=True, fillcolor='red')
c.circle(coord=[x,y+s], linecolor='red', fill=True, fillcolor='red')
c.circle(coord=[x,y+s+s], linecolor='red', fill=True, fillcolor='red')

x = 100
c.text(coord=[x,y], anchor='c,l', text='Anchor Is c,l', size=10)
c.text(coord=[x,y+s],  anchor='c,c', text='Anchor Is c,c', size=10)
c.text(coord=[x,y+s+s], anchor='c,h', text='Anchor Is c,h', size=10)

c.circle(coord=[x,y], linecolor='red', fill=True, fillcolor='red')
c.circle(coord=[x,y+s], linecolor='red', fill=True, fillcolor='red')
c.circle(coord=[x,y+s+s], linecolor='red', fill=True, fillcolor='red')

x = 190
c.text(coord=[x,y], anchor='r,l', text='Anchor Is r,l', size=10)
c.text(coord=[x,y+s], anchor='r,c', text='Anchor Is r,c', size=10)
c.text(coord=[x,y+s+s], anchor='r,h', text='Anchor Is r,h', size=10)

c.circle(coord=[x,y], linecolor='red', fill=True, fillcolor='red')
c.circle(coord=[x,y+s], linecolor='red', fill=True, fillcolor='red')
c.circle(coord=[x,y+s+s], linecolor='red', fill=True, fillcolor='red')

# finally, output the graph to a file
c.render()



