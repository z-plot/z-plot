#! /usr/bin/env python

# import the library
from zplot import *

# describe the drawing surface
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='example1', dimensions=['3in', '2.4in'])

# load some data
t = table(file='example1.data')

# make a drawable region for a graph
d = drawable(canvas=c, xrange=[0,10], yrange=[0,10],
             coord=['0.5in','0.4in'], dimensions=['2.3in','1.7in'])

# make some axes
axis(drawable=d, title='A Sample Graph', xtitle='The X-Axis',
     ytitle='The Y-Axis')

# plot the points
p = plotter()
p.points(drawable=d, table=t, xfield='x', yfield='y', style='triangle',
         linecolor='red', fill=True, fillcolor='red')

# finally, output the graph to a file
c.render()

