#! /usr/bin/env python

# import the library
from zplot import *

# describe the drawing surface
c = postscript(title='example2.eps', dimensions=['3in', '2.4in'])

# load some data
t = table(file='example2.data')
thi = table(table=t, where='y > 5')

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
p.points(drawable=d, table=thi, xfield='x', yfield='y', style='circle',
         linecolor='green', size='5', linewidth=2)
    
# finally, output the graph to a file
c.render()


