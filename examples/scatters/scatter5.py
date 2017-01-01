#! /usr/bin/env python

# should be in your PYTHONPATH or installed somewhere
from zplot import *

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='scatter5', dimensions=[300,300])
t = table(file='scatter5.data')
d = drawable(canvas=c, xrange=[0,80], yrange=[0,80], coord=[30,30],
             dimensions=[260,260])

axis(drawable=d, yauto=['','',10], xauto=['','',10])

p = plotter()
p.function(drawable=d, function=lambda x: x, xrange=[0,80], step=10,
           linewidth=0.25, linecolor='gray')

# now plot the intervals and points
p.points(drawable=d, table=t, xfield='x', yfield='y', style='label',
         labelfield='state', labelsize=9.0)

# now, do a closeup!
closeup = drawable(canvas=c, xrange=[51,53], yrange=[0,10],
                   coord=[220,100], dimensions=[100,70])

# this is UGLY -- but get all the data in the scrunhed-up area
t2 = table(table=t, where='(x>=50.9) and (x<=51.1)')

p.points(drawable=closeup, table=t2, xfield='x', yfield='rownumber',
         style='label', labelfield='state', labelsize=8.0)

c.box(coord=[[205,90],[235,190]], linecolor='red')
c.line(coord=[[205,190],[199,202]], linecolor='red', arrow=True,
       arrowlinecolor='red', arrowfillcolor='red')

c.render()




