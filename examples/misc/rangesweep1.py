#! /usr/bin/env python

# source the library; assumes it is in PYTHONPATH or installed
from zplot import *

t = table(file='rangesweep1.data')
c = postscript(title='rangesweep1.eps', dimensions=['4in','2.5in'])
d = drawable(canvas=c, dimensions=['3.5in','2.0in'],
             coord=['0.4in','0.4in'], xrange=[-20,80], yrange=[0,1])

p = plotter()
p.verticalfill(drawable=d, table=t, xfield='c0', yfield='c2', ylofield='c1',
               fillcolor='lightblue')
p.line(drawable=d, table=t, xfield='c0', yfield='c1', linecolor='blue')
p.line(drawable=d, table=t, xfield='c0', yfield='c2', linecolor='blue')

axis(drawable=d, yauto=['','',0.2], xauto=['','',20], xtitle='Temperature (c)',
     xtitlefont='Helvetica-Bold')

grid(drawable=d, x=False, yrange=[0.2,1.0], ystep=0.2, linedash=[4,2],
     linecolor='orange', linewidth=0.5)

# some labels
c.line(coord=d.map([[0,0.65], [0,0.4]]), arrow=True)
c.line(coord=d.map([[64,0.4], [64,0.63]]), arrow=True)

c.text(coord=d.map([0,0.67]), text='F1', rotate=90, anchor='l,c', size=6.0,
                   font='Helvetica-Bold')
c.text(coord=d.map([64,0.38]), text='F2', rotate=90, anchor='r,c', size=6.0,
                   font='Helvetica-Bold')

c.render()



