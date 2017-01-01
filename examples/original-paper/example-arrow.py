#! /usr/bin/env python

from zplot import *
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='example-arrow', dimensions=[180, 180])

off = 90
L = 60

asize = 1

for x,y in [[L,0], [L,L], [0,L], [-L,L], [-L,0], [-L,-L], [0,-L], [L,-L]]:
    if asize % 2 == 0:
        dofill = True
    else:
        dofill = False

    c.line(coord=[[off,off],[x+off,y+off]], linecolor='black', linewidth=1,
           arrow=True, arrowheadlength=2*asize, arrowheadwidth=asize,
           arrowlinewidth=0.5, arrowfill=dofill, arrowfillcolor='black')
    asize += 1

c.render()







