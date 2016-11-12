#! /usr/bin/env python

from zplot import *
import sys

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='km', dimensions=['4in','2.5in'])

d = drawable(canvas=c, xrange=[0,50], yrange=[0.0,1.0])
t = table('km.data')

p = plotter()
L = legend()
p.verticalfill(drawable=d, table=t, xfield='T', yfield='hi1', ylofield='lo1',
               fillcolor='lightblue', legend=L, legendtext='95% CI Group A')
p.verticalfill(drawable=d, table=t, xfield='T', yfield='hi2', ylofield='lo2',
               fillcolor='pink', legend=L, legendtext='95% CI Group B')
p.verticalfill(drawable=d, table=t, xfield='T', yfield='hi1', ylofield='lo2',
               fillcolor='lightgreen', legend=L, legendtext='Overlap of CIs')
p.line(drawable=d, table=t, xfield='T', yfield='val1', linecolor='blue',
       legend=L, legendtext='Group A')
p.line(drawable=d, table=t, xfield='T', yfield='val2', linecolor='red',
       legend=L, legendtext='Group B')

# axes, labels, legend
axis(drawable=d, yauto=['','',0.2], xauto=['','',12], xtitle='Months')
c.text(coord=d.map([25,1]), text='Kaplan-Meier Example', font='Courier')
L.draw(canvas=c, coord=[260,155], style='left', down=True, width=8,
       height=8, fontsize=8.0)

c.render()




