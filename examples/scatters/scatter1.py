#! /usr/bin/env python

from zplot import *

c = postscript(title='scatter1.eps', dimensions=['300','300'])

t = table(file='scatter1.data')
t.addcolumn(column='z', value=0)

d = drawable(canvas=c, xrange=[0,80], yrange=[0,80], coord=[10,10],
             dimensions=[285,285])

p = plotter()

p.function(drawable=d, function=lambda x: x, xrange=[0,80], step=10,
           linewidth=0.25, linecolor='gray')

p.points(drawable=d, table=t, xfield='x', yfield='y', style='triangle',
         linewidth=0.0, size=3.0, fill=True, fillcolor='red')

# Shows how easy it is to mark x and y axis with locations of the
# various data points; just redraw, set one value to zero, and use
# whatever symbol is appropriate (here, vline, hline)
p.points(drawable=d, table=t, xfield='x', yfield='z', style='vline',
         linecolor='black', linewidth=0.25, size=3.0)
p.points(drawable=d, table=t, xfield='z', yfield='y', style='hline',
         linecolor='black', linewidth=0.25, size=3.0)

axis(drawable=d, dolabels=False, domajortics=False, linewidth=0.25)

c.render()






