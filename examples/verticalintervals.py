#! /usr/bin/env python
import os

# pull in zplot from parent directory
CODE_DIR = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append(os.path.dirname(CODE_DIR))
from zplot import *

def main():
    # init table, canvas, drawable, and axis
    t = table(os.path.join(CODE_DIR,'data','throughput-range.dat'))
    canvas = postscript('verticalintervals.eps')
    d = drawable(canvas, coord=[50,30],
                 xrange=[0,t.getmax('nodes')], yrange=[0,900])
    axis(d,
         xtitle='Nodes', xauto=[0,t.getmax('nodes'),1],
         ytitle='Throughput (MB)', yauto=[0,900,300])

    # ylofield and yhifield specify the interval range
    p = plotter()
    p.verticalintervals(d, t, xfield='nodes', ylofield='min', yhifield='max')
  
    canvas.render()

if __name__ == '__main__':
    main()
