#! /usr/bin/env python

from zplot import *

t = table('horizontalintervals.data')
canvas = postscript('horizontalintervals.eps')
d = drawable(canvas, coord=[50,30], xrange=[0,900],
             yrange=[0,t.getmax('nodes')])
axis(d, xtitle='Throughput (MB)', xauto=[0,900,300],
     ytitle='Nodes', yauto=[0,t.getmax('nodes'),1])

# ylofield and yhifield specify the interval range
p = plotter()
p.horizontalintervals(d, t, yfield='nodes', xlofield='min', xhifield='max')
  
canvas.render()

