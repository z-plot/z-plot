#! /usr/bin/env python

from zplot import *

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='bars6', dimensions=[300,140])
d = drawable(canvas=c, xrange=[-0.5,2.5], yrange=[-5000,15000],
             dimensions=[260,80])
t = table(file='bars6.data')

# because tics and axes are different, call axis() twice, once to
# specify x-axis, the other to specify y-axis
axis(drawable=d, style='y', yauto=['','',5000])

axis(drawable=d, style='x', doaxis=False, domajortics=False,
     xmanual=[['ABC Corp', 0],['NetStuff',1],['MicroMason',2]],
     xaxisposition=-5000)

grid(drawable=d, x=False, ystep=5000, linecolor='salmon')

c.text(coord=d.map([-0.4,15500]), text='Annual Revenues (thousands)',
       anchor='l', font='Courier-Bold', size=9)

p = plotter()
p.verticalbars(drawable=d, table=t, xfield='rownumber', yfield='c0',
               fill=True, fillcolor='salmon', barwidth=0.7, yloval=0,
               linewidth=0.5, labelfield='c0', labelformat='$%s')

c.render()


