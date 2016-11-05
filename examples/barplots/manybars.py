#! /usr/bin/env python

import sys
from zplot import *

bartypes = [('hline', 1, 1),
            ('vline', 1, 1), 
            ('hvline', 1, 1), 
            ('dline1', 1, 2), 
            ('dline2', 1, 2),
            ('dline12', 0.5, 2),
            ('circle', 1, 2),
            ('square', 1, 1),
            ('triangle', 2, 2),
            ('utriangle', 2, 2)]

bartypes = [('hline', 1, 1),
            ('vline', 1, 1),
            ('hvline', 1, 1),
            ('dline1', 1, 2),
            ('dline2', 1, 2),
            ('dline12', 0.5, 2),
            ('circle', 1, 2),
            ('square', 1, 1),
            ('triangle', 2, 2),
            ('utriangle', 2, 2)]




L = len(bartypes)

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='manybars', dimensions=[L*10, 110])

d = drawable(canvas=c, xrange=[0,L+1], yrange=[0,10], coord=[0,5],
             dimensions=[L*10,100])

t = table(file='manybars.data')

p = plotter()
for btype, fsize, fskip in bartypes:
    p.verticalbars(drawable=d, table=t, xfield='c0', yfield='c1', fill=True,
                   fillcolor='darkgray', fillstyle=btype, barwidth=0.9,
                   fillsize=fsize, fillskip=fskip)
    t.update(set='c0=c0+1')


c.render()




