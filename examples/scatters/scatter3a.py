#! /usr/bin/env python

from zplot import *

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='scatter3a', dimensions=[300,300])

t = table(file='scatter3a.data')

d = drawable(canvas=c, xrange=[0,80], yrange=[0,80], coord=[30,30],
             dimensions=[260,260])

axis(drawable=d, yauto=['','',10], xauto=['','',10])

c.line(coord=d.translatecoord([[0,0],[80,80]]), linewidth=0.25,
       linecolor='gray')

p = plotter()
p.points(drawable=d, table=t, xfield='c0', yfield='c1', sizefield='c2',
         sizediv=3.0, style='circle', linewidth=0, fill=True,
         fillcolor='salmon')
p.points(drawable=d, table=t, xfield='c0', yfield='c1', sizefield='c2',
         sizediv=3.0, style='circle', linewidth=0.25)

c.render()

