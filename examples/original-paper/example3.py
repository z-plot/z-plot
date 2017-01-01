#! /usr/bin/env python

# import the library
from zplot import *

# describe the drawing surface
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='example3', dimensions=['3.3in', '2.4in'])

# load some data
t = table(file='example3.data')

# make a drawable region for a graph
d1 = drawable(canvas=c, xrange=[0,10], yrange=[0,10],
             coord=['0.5in','0.4in'], dimensions=['2.3in','1.7in'])
d2 = drawable(canvas=c, xrange=[0,10], yrange=[0,20],
             coord=['0.5in','0.4in'], dimensions=['2.3in','1.7in'])

# make some axes
axis(drawable=d1, title='A Sample Graph', xtitle='The X-Axis',
     ytitle='The Y-Axis')
axis(drawable=d2, style='y', title='', ytitle='The Second Y-Axis',
     yaxisposition=10, yauto=[0,20,4], labelstyle='in', ticstyle='in')
     

# plot the points
p = plotter()
p.points(drawable=d1, table=t, xfield='x', yfield='y', style='triangle',
         linecolor='red', fill=True, fillcolor='red')
p.points(drawable=d2, table=t, xfield='x', yfield='y', style='triangle',
         linecolor='green', fill=True, fillcolor='green')
    
# finally, output the graph to a file
c.render()

