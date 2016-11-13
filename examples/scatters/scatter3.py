#! /usr/bin/env python

from zplot import *

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='scatter3', dimensions=[310,310])
t = table(file='scatter3.data')

d = drawable(canvas=c, xrange=[0,80], yrange=[0,80], dimensions=[260,260],
             coord=[40,40])

axis(drawable=d, yauto=['','',10], xauto=['','',10])

c.line(coord=d.translatecoord([[0,0],[80,80]]), linewidth=0.25,
       linecolor='gray')

p = plotter()
p.points(drawable=d, table=t, xfield='c0', yfield='c1', style='circle',
         linewidth=0.25, fill=True, fillcolor='pink', size=5)

t.addcolumn(column='ta', value='A')
p.points(drawable=d, table=t, xfield='c0', yfield='c1', style='label',
         labelfield='ta', labelsize=6.0)

p.points(drawable=d, table=t, xfield='c1', yfield='c2', style='circle',
         linewidth=0.25, fill=True, fillcolor='yellow', size=5)
t.addcolumn(column='tb', value='B')
p.points(drawable=d, table=t, xfield='c1', yfield='c2', style='label',
         labelfield='tb', labelsize=6.0)

c.render()







