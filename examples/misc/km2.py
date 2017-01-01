#! /usr/bin/env python

# source the library; assumes it is in PYTHONPATH or installed
from zplot import *
import sys

# data
t = table(file='km2.data')

# canvas and a single drawable
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='km2', dimensions=['4in','2.5in'])
d = drawable(canvas=c, dimensions=['3.5in','2.0in'],
             coord=['0.4in','0.4in'], xrange=[0,36], yrange=[0.3,1])

# now plot the data
L = legend()
p = plotter()
p.verticalfill(drawable=d, table=t, xfield='T', yfield='hi1', ylofield='lo1',
               fillcolor='lightblue', legend=L, legendtext='95% CI')
p.verticalfill(drawable=d, table=t, xfield='T', yfield='hi2', ylofield='lo2',
               fillcolor='lightblue')
p.line(drawable=d, table=t, xfield='T', yfield='val1', linecolor='blue',
       legend=L, legendtext='Group A')
p.line(drawable=d, table=t, xfield='T', yfield='val2', linecolor='red',
       legend=L, legendtext='Group B')

# axes, labels, legend
axis(drawable=d, yauto=['','',0.1], xauto=['','',12], xtitle='Months',
     xtitlefont='Helvetica-Bold')
L.draw(canvas=c, coord=d.map([8,.5]), style='left')

# all done
c.render()





