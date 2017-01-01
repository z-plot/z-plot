#! /usr/bin/env python

# source the library; assumes it is in PYTHONPATH or installed
from zplot import *
import sys

all = table(file='rangesweep2.data')
a = table(table=all, where='c1 == \'a\'')
b = table(table=all, where='c1 == \'b\'')

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='rangesweep2', dimensions=[300, 250])
d = drawable(canvas=c, xrange=[0,120], yrange=[0,100], coord=[40,40],
             dimensions=[250,200])

p = plotter()
L = legend()
p.verticalfill(drawable=d, table=a, xfield='c0', yfield='c5', ylofield='c4',
               fillcolor='blue', legend=L, legendtext='Treatment A')
p.verticalfill(drawable=d, table=b, xfield='c0', yfield='c5', ylofield='c4',
               fillcolor='red', legend=L, legendtext='Treatment B')
p.line(drawable=d, table=a, xfield='c0', yfield='c2', linewidth=0.5)
p.line(drawable=d, table=b, xfield='c0', yfield='c2', linewidth=0.5,
       linedash=[4,2])
p.points(drawable=d, table=a, xfield='c0', yfield='c2', style='circle',
         fill=True, fillcolor='black', linewidth=0.25)
p.points(drawable=d, table=b, xfield='c0', yfield='c2', style='circle',
         linewidth=0.25)

axis(drawable=d, yauto=['','',10], xauto=['','',12],
     xtitle='Follow-up Time (months)', ytitle='Average Night Driving Score')
L.draw(canvas=c, coord=d.map([6,15]))

c.text(coord=d.map([60,100]), text='Average Night Driving Score', size=6)
c.text(coord=d.map([60,96]), size=6,
       text='With Missing Values Imputed Using Approximate Bayesian Bootstrap')
c.text(coord=d.map([60,92]), size=6,
       text='and 10% Lower on Average than Observed Values')

c.render()





