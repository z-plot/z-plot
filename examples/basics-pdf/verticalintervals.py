#! /usr/bin/env python

from zplot import *

t = table('verticalintervals.data')
canvas = pdf('verticalintervals.pdf')
d = drawable(canvas, coord=[50,30],
             xrange=[0,t.getmax('nodes')], yrange=[0,900])
axis(d, xtitle='Nodes', xauto=[0,t.getmax('nodes'),1],
     ytitle='Throughput (MB)', yauto=[0,900,300])

# ylofield and yhifield specify the interval range
p = plotter()
p.verticalintervals(d, t, xfield='nodes', ylofield='min', yhifield='max')
  
canvas.render()
