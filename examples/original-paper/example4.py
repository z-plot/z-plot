#! /usr/bin/env python

# import the library
from zplot import *

# describe the drawing surface
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='example4', dimensions=[380, 240])

# make a drawable region for a graph
d = drawable(canvas=c, xrange=[0,6], yrange=[0,11],
             coord=[50,50], dimensions=[250,150])

# make some axes
axis(drawable=d, title='Lots of Patterns', xtitle='The X-Axis', 
    ytitle='The Y-Axis')

# plot the points
b1 = table(file='example4.1.data')
b2 = table(file='example4.2.data')
b3 = table(file='example4.3.data')
b4 = table(file='example4.4.data')
b5 = table(file='example4.5.data')

L = legend()

p = plotter()
# note pattern of drawing tallest things first, then layering shorter
# things atop that, etc. - commonly used in bar graphs like this.
p.verticalbars(drawable=d, table=b5, xfield='x', yfield='y', fill=True, 
               fillcolor='darkgray', bgcolor='white', barwidth=0.9, legend=L,
               legendtext='Stuff', linewidth=0.5)
p.verticalbars(drawable=d, table=b4, xfield='x', yfield='y', fill=True, 
               fillstyle='dline1', bgcolor='white', barwidth=0.9, legend=L,
               legendtext='Things', linewidth=0.5)
p.verticalbars(drawable=d, table=b3, xfield='x', yfield='y', fill=True, 
               fillcolor='lightgrey', bgcolor='white', barwidth=0.9, legend=L,
               legendtext='Junk', linewidth=0.5)
p.verticalbars(drawable=d, table=b2, xfield='x', yfield='y', fill=True, 
               fillstyle='triangle', bgcolor='white', barwidth=0.9, fillsize=4,
               fillskip=2, legend=L, legendtext='Yards', linewidth=0.5)
p.verticalbars(drawable=d, table=b1, xfield='x', yfield='y', fill=True, 
               fillcolor='mintcream', bgcolor='white', barwidth=0.9, legend=L,
               legendtext='Dogs', linewidth=0.5)

L.draw(canvas=c, coord=d.map([6,8]), down=True, width=15, height=15)

c.render()


